import whisper
import requests
import os
import wave
import pyaudio
import string
from fuzzywuzzy import fuzz
import nltk
from nltk.corpus import cmudict

from config import Config

if Config.MOCK_SPEAKER:
    from mocks.speak_txt import speak
else:
    from speak_txt import speak

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


def record_audio(filename, duration=5, sample_rate=16000):
    chunk = 1024
    channels = 1
    format = pyaudio.paInt16

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)

    print(f"Recording for {duration} seconds...")

    frames = []
    for _ in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording complete. Saving audio...")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))


nltk.download('cmudict')
nltk.download('punkt')

d = cmudict.dict()


def transcribe_audio(filename, model):
    print("Transcribing audio...")
    result = model.transcribe(filename)
    text = result['text'].strip().lower()

    cleaned_text = remove_punctuation(text)

    words = cleaned_text.split()

    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if are_similar_sounding(words[i], words[j]):
                return words[i]
                print(f"Words '{words[i]}' and '{words[j]}' are phonetically similar!")

    return cleaned_text


def remove_punctuation(text):
    """
    Remove punctuation from the given text.
    """
    return text.translate(str.maketrans('', '', string.punctuation))


def get_phonetic_representation(word):
    """
    Get the phonetic representation of a word using CMU Pronouncing Dictionary.
    Returns a list of phonetic symbols (phones) or None if not found.
    """
    word = word.lower()
    if word in d:
        return d[word][0]  
    return None

def are_similar_sounding(word1, word2):
    """
    Check if two words are phonetically similar.
    Uses CMU Pronouncing Dictionary to compare the phonetic representations of words.
    """
    word1 = "cap"
    phonetic1 = get_phonetic_representation(word1)
    phonetic2 = get_phonetic_representation(word2)
    
    if phonetic1 and phonetic2:
        return fuzz.ratio("".join(phonetic1), "".join(phonetic2)) > 80  
    return False



def extract_object_name(query_text):
    """
    Extracts the object name from the query text.
    This is a simple example where the object name is assumed to be the part of the query
    after 'find'. Modify it based on your actual query structure.
    """
    # We can make this better by enhancing this function with more sophisticated
    #  parsing, NLP, or regex to handle different scenarios.
    if "find" in query_text:
        parts = query_text.split("find", 1) 
        if len(parts) > 1:
            return parts[1].strip()
    return None


def listen_and_process():
    while True:
        audio_file = "temp_audio.wav"
        record_audio(audio_file, duration=5)

        try:
            query_text = transcribe_audio(audio_file, whisper_model)
            print("You said:", query_text)

            if "hey, cap" in query_text:
                object_name = extract_object_name(query_text) 
                
                if object_name:
                    response_phrase = f"I want to find {object_name}"
                    print(response_phrase)

                    speak(response_phrase)
                    print(f"Sending query to the server with object: {object_name}")
                    
                    response = send_mic_query(response_phrase)
                    speak(response) 
                else:
                    speak("Sorry, I couldn't detect the object name.")

            else:
                print("Activation phrase not detected.")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Clean up the temporary audio file
            if os.path.exists(audio_file):
                os.remove(audio_file)


# Load the Whisper model
whisper_model = whisper.load_model("base")

mic_url = Config.URL + "/speech_query"
token = read_token_file()

if __name__ == "__main__":
    try:
        listen_and_process()
    except KeyboardInterrupt:
        print("\nExiting gracefully.")