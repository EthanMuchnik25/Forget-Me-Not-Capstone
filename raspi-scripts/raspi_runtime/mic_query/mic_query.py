import speech_recognition as sr
import requests
import os
from config import Config
if Config.MOCK_SPEAKER:
    from mocks.speak_txt import speak
else:
    from speak_txt import speak

# NOTE: create creds.txt in the local directory for this to work. It should have
#  the username and password for a existing user


# NOTE: This is all very primitive logic for speech querying, and not very good.
#  I made this trach bc we will probably rewrite it. However, it works for 
#  demonstration purposes.

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


def send_mic_query(query_text):
    global token
    global mic_url

    headers = {'Authorization': f'Bearer {token}'}
    body = {'query': query_text}

    response = requests.post(mic_url, headers=headers, json=body)
    if response.status_code == 200:
        raise Exception("Failed to reauthenticate")
    
    print(f"error sending request: {response.status_code}  Response: {response.text}")
    print("Attempting reauthentication")

    if not reauthenticate():
        raise Exception("Failed to reauthenticate")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(mic_url, headers=headers, json=body)
    if response.status_code != 200:
        print(f"Failed to send after reauthentication: {response.status_code}  Response: {response.text}")

    return response.json().get('msg')



# Function to continuously listen and print speech
def listen_and_print():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")

        while True:
            try:
                # Capture audio
                print("Speak now:")
                audio = recognizer.listen(source)

                # Recognize speech using Google Web Speech API
                text = recognizer.recognize_google(audio).lower()
                print("You said: " + text)

                # Check if the activation phrase is spoken
                if "hello capstone" in text:
                    speak("Sending query to the server!!!")
                    print("Activation phrase detected!")
                    response = send_mic_query(text)
                    speak(response)
                else:
                    print("Activation phrase not detected.")

            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")


# Initialize recognizer
recognizer = sr.Recognizer()

mic_url = Config.URL + "/speech_query"
token = read_token_file()

if __name__ == "__main__":
    try:
        while True:
            listen_and_print()
    except KeyboardInterrupt:
        print("\nExiting gracefully.")
