## About
Originally forked from [FASText](https://github.com/MichalBusta/FASText) July 20, 2017, which is based on paper *FASText: Efficient Unconstrained Scene Text Detector,Busta M., Neumann L., Matas J.:  ICCV 2015.*, [`pdf`](http://cmp.felk.cvut.cz/~neumalu1/neumann_iccv2015.pdf)

## Installation
Run the following

``` shell
bash install.sh
```

### Prerequisites
- OpenCV
- Anaconda for python2

After building the executables, you can use toy examples in python:
```
cd tools
python segmentation.py <path_to_image>
```
  - will process and draw FASText keypoints on scale pyramid.

```
cd tools
python evaluateSegmentation.py
```
  - will reproduce results on ICDAR 2013 dataset (requires Challenge 2 dataset & GT segmentations)

For text lines clustering, you can run the simple demo:
```
cd tools
python testLines.py
```
The text line clustering is just simple voting in Hough space where each region vote for each line going through region centroid

Please cite this paper if you use this data or code:
```
@InProceedings{Busta_2015_ICCV,
  author = {Busta, Michal and Neumann, Lukas and Matas, Jiri},
  title = {FASText: Efficient Unconstrained Scene Text Detector},
  journal = {The IEEE International Conference on Computer Vision (ICCV)},
  month = {June},
  year = {2015}
}
```
