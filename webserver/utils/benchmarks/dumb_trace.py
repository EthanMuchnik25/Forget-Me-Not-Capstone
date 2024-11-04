import argparse
import sys
import time
sys.path.append('../')
from helper.authenticate import register_and_login
from helper.send_to_api import *
from scripts.send_jpg_dir import send_jpgs_from_dir

# This file will just call each function 10 times one after the other.


parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, default=10, help='Max iterations of each call')
parser.add_argument('-s', type=str, default="http://localhost:4000", help='Server URL')

args = parser.parse_args()


uname = 'fquioeyncvlsiuecnfwpercm'
pw = 'a;pew9ifmpwoeirj,fjargre'
server_url = args.s
iters = args.n


token = register_and_login(server_url, uname, pw)

for i in range(iters):
    send_simple(server_url)

for i in range(iters):
    send_test_auth(server_url, token)

# Send jpgs
send_jpgs_from_dir(server_url, token, "../imgs", iters)

# If we query too soon the models won't have run yet??
time.sleep(5)

# Recieve jpgs
links = []
for i in range(iters):
    res = send_text_query(server_url, token, "person", i)
    if res != None:
        links.append(res)

# Fetch links
for i in range(iters):
    send_get_room_img(server_url, token, links[i%len(links)])

# TODO maybe have speech query later

