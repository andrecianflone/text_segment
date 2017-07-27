import codecs
import os
import sys
import json
import numpy as np
import cv2
import argparse
from ft import FASTex

BASE = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def settings(path):
  """ Returns settings dictionary """
  with codecs.open(path, encoding='utf-8') as f:
    settings = json.load(f)
  return settings

def drawCharBoxes(img, segmentations, max_boxes=200):
  """ Draw all character boxes on image """
  for i in range(segmentations.shape[0]):
    pt1 = (segmentations[i][0], segmentations[i][1])
    pt2 = (pt1[0] + segmentations[i][2], pt1[1] + segmentations[i][3])
    cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
    if max_boxes is not None and i >= max_boxes: break;

if __name__ == "__main__":
  default_img = BASE + "/sample/arnie.jpg"
  parser = argparse.ArgumentParser(description=__doc__,
                          formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('--image', default=default_img, type=str, help='Image to parse')
  # parser.add_argument('--file_save', help='Save results of search to this json')
  args = parser.parse_args()

  # Verify image
  if not os.path.isfile(args.image):
    sys.exit("Image not found")

  if not args.image.endswith(".png") and not args.image.endswith(".jpg"):
    sys.exit("Not valid image")

  settings = settings("config.json")
  output_dir = settings['debug_dir']
  ft = FASTex(edgeThreshold=13, nlevels=-1, minCompSize = 4)

  # Read image as numpy array
  img = cv2.imread(args.image, 0) # load image in grayscale, i.e. 1 channel
  img_o = cv2.imread(args.image)
  img3 = cv2.imread(args.image)

  # Get boxes of characters
  # Elem in rows:: [bbox.x, bbox.y, bbox.width, bbox.height, keyPoint.pt.x, keyPoint.pt.y, octave, ?, duplicate, quality, [keypointsIds]]
  segmentations = ft.getCharSegmentations(img, output_dir, 'base')

  drawCharBoxes(img3, segmentations)
  cv2.imwrite(output_dir + "/rect2.jpg", img3)

  # Get boxes of text lines, should be a lot less than characters
  # Elem in rows [bbox.x, bbox.y, bbox.width, bbox.height, rotated rectangle points (pt1.x, pt1.y, ... pt3.y) ]
  txt_lines = ft.findTextLines(output_dir, 'txt_lines')

  pass

