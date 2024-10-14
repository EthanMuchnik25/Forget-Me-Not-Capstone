from picamzero import Camera
from config import Config

cam = Camera()

def capture_image():
  # If temp img name reused add to config
  temp_img_name = "imgs/temp_img.jpg"
  cam.take_photo(temp_img_name)
  return temp_img_name

