# NOTE: This will be missing some of the APIs I don't think will be particularly
#  useful to have standard functions for. Feel free to add functions you think
#  will be useful

import requests

def token_header(token):
    return {'Authorization': f'Bearer {token}'}


# =============== Authentication routes ===============

def send_test_auth(server_url, token):
    auth_url = server_url + '/test_auth'
    response = requests.get(auth_url, headers=token_header(token))
    if response.ok:
        return True
    else:
        print('Testing authentication error: ',response.text)
        return False


def send_login(server_url, uname, pw):
    login_url = server_url + "/login"
    payload = {
        'username': uname,
        'password': pw
        }
    response = requests.post(login_url, json=payload)

    if response.ok:
        token = response.json().get('access_token')
        return token
    elif response.status_code == 400:
        print('Login failed:', response.json().get('msg'))
        return None
    else:
        print('Unexpected login error:', response.status_code, response.text)
        return None
    

def send_register(server_url, uname, pw):
    register_url = server_url + "/register"
    payload = {
        'username': uname,
        'password': pw
        }
    response = requests.post(register_url, json=payload)

    if response.ok:
        return True
    else:
        print('Registration error: ', response.text)
        return False
    

def send_logout(server_url, token):
    logout_url = server_url + '/logout'
    response = requests.post(logout_url, headers=token_header(token))
    if response.ok:
        return True
    else:
        print('Logout error: ', response.text)
        return False
    

def send_deregister(server_url, token):
    logout_url = server_url + '/deregister'
    response = requests.post(logout_url, headers=token_header(token))
    if response.ok:
        return True
    else:
        print('Deregister error: ', response.text)
        return False



# ========================== App routes ==========================


def send_simple(server_url):
    simple_url = server_url + "/simple"
    response = requests.get(simple_url)
    if response.ok:
        return True
    else:
        print("Simple error: ", response.text)
        return False
    

# TODO API subject to change...
def send_text_query(server_url, token, query: str, index: int):
    query_url = f"{server_url}/text_query?query={query}&index={index}"
    response = requests.get(query_url, headers=token_header(token))
    if response.ok:
        img_url = response.json().get('imageUrl')
        return img_url
    else:
        print('Send text query error: ',response.text)
        return None


def send_get_room_img(server_url, token, img_url):
    room_img_url = server_url + img_url
    response = requests.get(room_img_url, headers=token_header(token))
    if response.ok:
        # Returns bytes
        return response.content
    else:
        print("Error get_room_img: ", response.text)
        return None
    

# Note: This takes a file handle, not a path
def send_post_img(server_url, token, img_file_handle):
    post_img_url = server_url + '/post_img'
    # NOTE: If we decide to change the api we will have to change this
    files = {'file': img_file_handle}
    response = requests.post(post_img_url, headers=token_header(token), files=files)
    if response.ok:
        return True
    else:
        print("Error posting image: ", response.text)
        return False


def send_speech_query(server_url, token, query: str):
    speech_query_url = server_url + '/speech_query'
    body = {'query': query}
    response = requests.post(speech_query_url, headers=token_header(token), json=body)
    if response.ok:
        # TODO possibly brittle
        res_str = response.json().get('msg')
        return res_str
    else:
        print("Error send_speech_query: ", response.text)
        return None