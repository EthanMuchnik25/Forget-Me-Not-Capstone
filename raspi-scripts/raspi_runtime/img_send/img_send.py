# This file periodically takes photos and sends them to the web server
import requests
from config import Config
import time
if Config.CAMERA_VER == "LAPTOP":
  # TODO implement laptop camera version
  from laptop_img_capture import capture_image
elif Config.CAMERA_VER == "RPI":
  from pi_img_capture import capture_image
elif Config.CAMERA_VER == "MOCK":
    from mocks.img_capture import capture_image
else:
    raise NotImplementedError


img_url = Config.URL + "/post_img"

while True:
  start_time = time.time()

  img_path = capture_image()

  img_file = open(img_path, 'rb')
  # TODO does this warrant a rename?
  files = {'file': img_file}

  response = requests.post(img_url, files=files)
  if not response.status_code == 400:
    print("error sending image")

  elapsed_time = time.time() - start_time

  # Ensure image rate is consistent
  time.sleep(max(0,Config.SECS_PER_IMG - elapsed_time))