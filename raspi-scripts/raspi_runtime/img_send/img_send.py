# This file periodically takes photos and sends them to the web server
import requests
import os

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

# TODO some of this logic seems to be duplicated among different files, namely 
#  things that keep running on the raspberry pi. Consider making a module for it
def read_creds_file():
    with open(Config.CREDS_FILE_PATH, "r") as file:
        uname = file.readline().strip()
        pw = file.readline().strip()
        return (uname, pw)
    raise Exception("Failed acquiring credentials from file. Does file exist?")


def read_token_file():
    if not os.path.exists(Config.TOKEN_FILE_PATH):
        with open(Config.TOKEN_FILE_PATH, "w") as file:
            file.write("")

    with open(Config.TOKEN_FILE_PATH, "r") as file:
        token = file.readline().strip()
        return token
    raise Exception("Failed acquiring token from file")


def write_token_file(new_token):
    with open(Config.TOKEN_FILE_PATH, "w") as file:
        file.write(new_token)

def set_new_token(new_token):
    global token
    write_token_file(new_token)
    token = new_token

def reauthenticate():
    login_url = Config.URL + "/login"
    uname, pw = read_creds_file()
    payload = {
        'username': uname,
        'password': pw
        }
    response = requests.post(login_url, json=payload)

    if response.status_code == 200:
        print('Login successful!')
        print('Access token:', response.json().get('access_token'))
        set_new_token(response.json().get('access_token'))
        return True
    elif response.status_code == 400:
        print('Login failed:', response.json().get('msg'))
    else:
        print('Unexpected error:', response.status_code, response.text)
    return False


def send_img_req(img_file):
    global token
    global img_url

    files = {'file': img_file}
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.post(img_url, headers=headers, files=files)
    if response.status_code == 200:
        return

    print(f"error sending image: {response.status_code}  Response: {response.text}")
    print("Attempting reauthentication")

    # Case code 401, unauthenticated
    
    if not reauthenticate():
        raise Exception("Failed to reauthenticate")

    img_file.seek(0)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(img_url, headers=headers, files=files)
    if response.status_code != 200:
        print(f"Failed to send after reauthentication: {response.status_code}  Response: {response.text}")


img_url = Config.URL + "/post_img"
# TODO do we have this in prod? Refactor this accordingly
# token = read_token_file()
token = ""

while True:
    start_time = time.time()

    img_path = capture_image()

    with open(img_path, 'rb') as img_file:
        send_img_req(img_file)

    elapsed_time = time.time() - start_time

    # Ensure image rate is consistent
    time.sleep(max(0,Config.SECS_PER_IMG - elapsed_time))
    
    print("pic_complete")