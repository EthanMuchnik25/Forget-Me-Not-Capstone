## Raspi specs:

### Images:

#### Onboard

The python commands available for the raspi camera are succinctly explained in [../small_scripts/camera_onboard.py](../small_scripts/camera_onboard.py)

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

TODO TBD onboard and specs