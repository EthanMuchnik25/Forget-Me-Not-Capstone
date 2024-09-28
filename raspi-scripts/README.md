# Raspi Scripts

This file will document what each of the relevant scripts are, how to run them, and some relevant information regarding properties of the data we are trying to acquire from the raspberry pi.

#### Quick Notes:
This directory does not use a virtual environment because these are all random test scripts, that don't need to be robust or absolutely always work for everyone.

__Fun fact__: If you plug your fan into the 5V and Ground pins, and point it at the heat sinks, the rpi will run substantially faster!

## Raspi specs:

### Images:

#### Install
To begin taking photos, follow the following documentation: [Important Link](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/0)

Alternatively, if you don't like reading, just type the following commands into your terminal, and you'll be able to use the appropriate command line scripts and python library:
```
sudo apt update
sudo apt install python3-picamzero
```

#### Specs

Here is a specsheet: [Important Link](https://www.raspberrypi.com/documentation/accessories/camera.html#hardware-specification)\
I have recorded some of the basic specs below, but more advanced specs such as video recording resolution modes can be found in the specshet.

| Property | Val |
| ---------- | ----- |
| (My) Model | Raspberry Pi Camera Module 3 Wide |
| Dimensions (max) | 4608 x 2592 pixels |
| Size | 1.1 MB (probably depens on compressability) |
| Time per image (single) | < 2.5s reliably |
| Time per image (sequence) | probably faster than otherwise |

Notes:\
Single image capture takes a long time, and may be limited by factors such as SD card BW or camera latency. It may be worth investigating what factors may cause it to take less time.


### Microphone

TODO TBD


## Script Documentation

Note: When making a script for the camera, you are never allowed to call it `picamzero.py`.

### `camera_onboard.py`
This script showcases most of the availabile configuration options when taking photos/videos with the raspberry pi. I think looking at this file is more useful than actual documentation.\
Probably don't actually run this file.

### `gen_trial_imgs.py`
This script takes a set of images in a way that simulates regular operation of the camera. Feel free to duplicate or modify if you wish to adjust parameters such as resolution, image capture frequency, or the image levels.

### TODO?
Eventually we should probably add scripts which:
- Simulate final operation [pic: (take picture, run preprocessing, send to server) + (mic detect speech, send query, output result) ]
- Possibly attempt to run the model locally to see if the rpi can cope with the workload
- Test microphone capability




