from helper.send_to_api import send_login, send_register


def register_and_login(server_url, uname, pw):
    print("Registering and logging in")
    token = send_login(server_url, uname, pw)
    
    if token == None:
        # I think it is ok if the user already exists
        send_register(server_url, uname, pw)
        # if not send_register(server_url, uname, pw):
            # raise Exception("Fatal error could not register user")
        token = send_login(server_url, uname, pw)
        if token == None:
            raise Exception("Fatal error could not login user after successful registration")
    print("Successfully registered and logged in")
    return token