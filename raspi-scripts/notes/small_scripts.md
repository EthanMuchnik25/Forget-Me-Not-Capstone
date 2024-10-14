# Small Scripts Documentation

This file will document what each of the relevant scripts are, how to run them, and some relevant information regarding properties of the data we are trying to acquire from the raspberry pi.

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