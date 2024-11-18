# Pruning Notes

## Intro

This file will probably just contain observations I notice while writing the code to save memory/compute in the cases where we do not need to do them.


By nature, the optimization code will contain some amount of thresholding, and I will attempt to explain my observations here.

## Directory

All these scripts are sort of all over the place, but I think this is ok because I don't plan on reusing them.

- generate_inferences.py: Creates a text file containing all inference results for images in a directory. I do this so I don't have to run expensive inference any time I want to run a test.
- compare_adj_diffs.py: Generates files containing pixel differences between adjacent images in a image trace directory
- mse_stats.py: Generates plots of pixel difference frequencies
- mse_thresh.py: File to help pick threshold for pixel difference metric

## Not Intro

### Pixel Difference

#### SSIM

Literally slower than YOLO inference on my laptop. This is a non-starter

#### Difference

Ok, but not as clear of a threshold as with MSE. Can generate graphs with mse_stats.py.

#### MSE

just google the formula :P

Here is a threshold value: 28

Here are some stats to go with it:
-> actually just check `mse_thresh.py` they are commented at the bottom



