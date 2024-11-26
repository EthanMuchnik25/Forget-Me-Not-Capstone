import os
import argparse
import sys
import time
sys.path.append('../')
from helper.send_to_api import send_post_img, send_deregister
from helper.authenticate import register_and_login



def send_all_jpgs_from_dir(server_url, token, directory, interval):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.jpg'):
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as file:
                    start_time = time.time()
                    if not send_post_img(server_url, token, file):
                        raise Exception("Error sending image from directory")

                    count += 1
                    print(f"Send successful: {count}")
                    elapsed_time = time.time() - start_time
                    time.sleep(max(0,interval - elapsed_time))


# TODO make this not shit the bed when there are 0 imgs
def send_jpgs_from_dir(server_url, token, directory, count, interval):
    curr = 0
    while curr < count:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.jpg'):
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as file:
                        if curr == count:
                            return
                        
                        start_time = time.time()
                        if not send_post_img(server_url, token, file):
                            raise Exception("Error sending image from directory")
                        
                        curr += 1
                        print(f"Send successful: {curr}")
                        elapsed_time = time.time() - start_time
                        time.sleep(max(0,interval - elapsed_time))



# Call with n=-1 for all photos
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=-1, help='Max number of pictures to send')
    parser.add_argument('-s', type=str, default="http://localhost:4000", help='Server URL')
    parser.add_argument('-i', type=int, default=0, help="Number of seconds between images")

    args = parser.parse_args()

    server_url = args.s
    count = args.n
    interval = args.i

    # Too lazy for robust soln, pick something no one will pick
    uname = "society"
    pw = "society"

    dir = "../../../Images"

    token = register_and_login(server_url, uname, pw)
    
    if count == -1:
        send_all_jpgs_from_dir(server_url, token, dir, interval)
    else:
        send_jpgs_from_dir(server_url, token, dir, count, interval)

    # send_deregister(server_url, token)



if __name__ == '__main__':
    main()


