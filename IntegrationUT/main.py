import sys 

sys.path.append('../webserver/utils/')

from helper.send_to_api import send_text_query
from helper.authenticate import register_and_login

def main():
    server_url = "http://localhost:4000"

    uname = 'soos'
    pw = 'ciety'

    token = register_and_login(server_url, uname, pw)

    result = send_text_query(server_url, token, "pencil", 0)
    print(result)


if __name__ == "__main__":
    main()