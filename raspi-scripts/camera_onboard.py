from picamzero import Camera
from time import sleep

cam = Camera()

# For preview:
cam.start_preview()
# Keep the preview window open for 5 seconds
sleep(5)
cam.take_photo("./temp_images/image.jpg")

# Captures a sequence of images at a given interval
cam.capture_sequence("./temp_images/sequence.jpg", num_images=3, interval=2)

# Captures a video of a given duration
cam.record_video("./temp_images/new_video.mp4", duration=5)


# To rotate camera:
cam.flip_camera(hflip=True, vflip=True)

# Adjust image resolution:
cam.still_size = (2592, 1944)

# Adjust the resolution of the preview
cam.preview_size = (1920, 1080)

# Add text to image. Can ajust thing like positoin, size, font, color, etc.
cam.annotate("top text")

# Set image to greyscale
cam.greyscale = True

# Alter the image levels
cam.gain = 1.0
cam.contrast = 2
cam.exposure = 1000000
cam.brightness = 0.2
cam.white_balance = 'cloudy'

cam.stop_preview()

# Additional effects can be applied after taking a photo using the cv2 library

