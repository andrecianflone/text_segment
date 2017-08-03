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

def drawCharBox(img, segmentations, idx):
  """ Draw box on array image img, using coordinates from segmentations[idx]"""
  pt1 = (segmentations[idx][0], segmentations[idx][1])
  pt2 = (pt1[0] + segmentations[idx][2], pt1[1] + segmentations[idx][3])
  cv2.rectangle(img, pt1, pt2, (0, 0, 255), 1)

def drawCharBoxes(img, segmentations, start_idx=0, max_boxes=None):
  """
  Draw all character boxes on image
  Args:
    max_boxes - max number of boxes to draw
  """
  for i in range(start_idx, segmentations.shape[0]):
    drawCharBox(img, segmentations, i)
    if max_boxes is not None and i >= start_idx + max_boxes: break;

def drawCharMask(img, ft, segmentations, idx):
  """ Draw character mask on img with mask idx corresponding to character
  from segmentations[idx]"""
  mask = ft.getSegmentationMask(idx)
  mask_inv = cv2.bitwise_not(mask)
  rows, cols = mask.shape
  x = segmentations[idx][0] # where mask starts in original image
  y = segmentations[idx][1] # where mask starts in original image
  roi = img[y:y+rows, x:x+cols]

  # Background from original
  bg = cv2.bitwise_and(roi,roi,mask=mask_inv)

  # Foreground with color
  fill = np.zeros((rows, cols, 3), dtype='uint8')
  fill[:,:] = np.array([0,255,0]) # green
  fg = cv2.bitwise_and(fill, fill, mask=mask)
  dst = cv2.add(bg,fg)
  img[y:y+rows, x:x+cols] = dst

def drawCharMasks(img, ft, segmentations, start_idx=0, max_chars=None):
  """
  Args:
    max_boxes - max number of boxes to draw
  """
  bg_mask = np.full((img.shape[0], img.shape[1]), 255, dtype='uint8')
  fg_mask = np.zeros((img.shape[0], img.shape[1]), dtype='uint8')
  for idx in range(start_idx, segmentations.shape[0]):
    mask = ft.getSegmentationMask(idx)
    mask_inv = cv2.bitwise_not(mask)
    rows, cols = mask.shape
    x = segmentations[idx][0] # where mask starts in original image
    y = segmentations[idx][1] # where mask starts in original image
    bg_mask[y:y+rows, x:x+cols] = mask_inv
    fg_mask[y:y+rows, x:x+cols] = mask
    if max_chars is not None and idx >= start_idx + max_chars: break;

  # Background from original
  bg = cv2.bitwise_and(img,img,mask=bg_mask)

  # Foreground with color
  fill = np.zeros((img.shape[0],img.shape[1], 3), dtype='uint8')
  fill[:,:] = np.array([0,255,0]) # green
  fg = cv2.bitwise_and(fill, fill, mask=fg_mask)
  dst = cv2.add(bg,fg)
  img[:,:,:] = dst

def viz_location(img_o, ft, segmentations, cumulative=False, max_chars=None):
  '''
  Save char boxes and masks to debug
  Args:
    cumulative - if true each image includes previous masks
  '''
  img = img_o
  step=100
  for i in range(0,max_chars + 1, step):
    if cumulative==False:
      img = np.copy(img_o)
    drawCharMasks(img, ft, segmentations, start_idx=i, max_chars=step+1)
    drawCharBoxes(img, segmentations, start_idx=i, max_boxes=step+1)
    name = "{}/box_{}-{}.jpg".format(output_dir, i, i + step)
    cv2.imwrite(name, img)

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

  viz_location(img3, ft, segmentations, cumulative=True, max_chars=2000)
  # drawCharMasks(img3, ft, segmentations, 100)
  # drawCharBoxes(img3, segmentations, 100)
  # cv2.imwrite(output_dir + "/mask.jpg", img3)

  # Get boxes of text lines, should be a lot less than characters
  # Elem in rows [bbox.x, bbox.y, bbox.width, bbox.height, rotated rectangle points (pt1.x, pt1.y, ... pt3.y) ]
  txt_lines = ft.findTextLines(output_dir, 'txt_lines')

  pass

