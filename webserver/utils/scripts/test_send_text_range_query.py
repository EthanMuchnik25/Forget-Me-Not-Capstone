# Extremely basic script that just tests the send_text_range_query endpoint

import sys

sys.path.append('../')
from helper.send_to_api import send_text_range_query
from helper.authenticate import register_and_login


def main():
    server_url = "http://localhost:4000"

    uname = 'weoiuwevxcmawlakdfhaklawyhlkahmdkvjhvfgfwjsd'
    pw = 'fdpiuyeouldfmvbfdsrespoij485734uhfwlkdovbj'

    token = register_and_login(server_url, uname, pw)

    result = send_text_range_query(server_url, token, "garbage", 0, 10)

    print(result)


if __name__ == "__main__":
    main()
