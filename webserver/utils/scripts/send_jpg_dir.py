import os
import argparse
import sys
sys.path.append('../')
from helper.send_to_api import send_post_img, send_deregister
from helper.authenticate import register_and_login



def send_all_jpgs_from_dir(server_url, token, directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.jpg'):
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as file:
                    if not send_post_img(server_url, token, file):
                        raise Exception("Error sending image from directory")


def send_jpgs_from_dir(server_url, token, directory, count):
    curr = 0
    while curr < count:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.jpg'):
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as file:
                        if curr == count:
                            return
                        if not send_post_img(server_url, token, file):
                            raise Exception("Error sending image from directory")
                        curr += 1



# Call with n=-1 for all photos
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=4, help='Max number of pictures to send')
    parser.add_argument('-s', type=str, default="http://localhost:4000", help='Server URL')

    args = parser.parse_args()

    server_url = args.s
    count = args.n

    # Too lazy for robust soln, pick something no one will pick
    uname = "asdlkjhfvnoieaufcynoiqwuefhmiawehm"
    pw = ";dvoj;ljvl;kjvc;lzkjxcv;lzcx mv;lzkjxcvml;z"

    dir = "../imgs"

    token = register_and_login(server_url, uname, pw)
    
    if count == -1:
        send_all_jpgs_from_dir(server_url, token, dir)
    else:
        send_jpgs_from_dir(server_url, token, dir, count)

    send_deregister(server_url, token)



if __name__ == '__main__':
    main()


