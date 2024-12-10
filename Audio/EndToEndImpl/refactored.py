import sounddevice as sd
import numpy as np
import whisper
import time
from multiprocessing import Queue, Process, Value
from enum import Enum
import requests
from config import Config
import os
from PIL import Image
from io import BytesIO
import asyncio
import websockets
import functools
from macSpeaker import speak
if Config.SPEECH_ENGINE == "MAC":
    from macSpeaker import speak
elif Config.SPEECH_ENGINE == "GOOGLE":
    from googlespeak import speak_text as speak
# from googlespeak import speak_text as speak

class State(Enum):
    INTAKING_QUERY = 1
    LISTENING_FOR_FRANK = 2
    NOT_LISTENING = 3

def read_creds_file():
    with open(Config.CREDS_FILE_PATH, "r") as file:
        uname = file.readline().strip()
        pw = file.readline().strip()
        return (uname, pw)
    raise Exception("Failed acquiring credentials from file. Does file exist?")

def write_token_file(new_token):
    with open(Config.TOKEN_FILE_PATH, "w") as file:
        file.write(new_token)


def set_new_token(new_token):
    write_token_file(new_token)

def read_token_file():
    if not os.path.exists(Config.TOKEN_FILE_PATH):
        with open(Config.TOKEN_FILE_PATH, "w") as file:
            file.write("")
    
    with open(Config.TOKEN_FILE_PATH, "r") as file:
        token = file.readline().strip()
        return token
    raise Exception("Failed acquiring token from file")

# def listen(audio_queue, state):
#     print("Starting audio listening process...")
#     sample_rate = 16000
#     recording_data = []
    
#     def audio_callback(indata, frames, time, status):
#         recording_data.append(indata.copy())

#     try:
#         with sd.InputStream(callback=audio_callback, 
#                           samplerate=sample_rate,
#                           channels=1,
#                           dtype=np.float32):
#             print("\nRecording... (Press Ctrl+C to stop)")
            
#             while True:
#                 current_state = state.value
#                 if current_state in [State.LISTENING_FOR_FRANK.value, State.INTAKING_QUERY.value]:
#                     recording_data.clear()
#                     time.sleep(2)
                    
#                     # if current_state == State.INTAKING_QUERY.value:
#                     #     print("listening")

#                     if recording_data:
#                         # print("\nProcessing audio chunk...")
#                         audio = np.concatenate(recording_data, axis=0)
#                         audio = audio.flatten()
#                         audio_queue.put(audio)

#     except KeyboardInterrupt:
#         print("\nRecording stopped")
#     except Exception as e:
#         print(f"\nError in listen process: {e}")


def listen(audio_queue, state):
    """
    Starts the WebSocket server to listen for audio data sent
    from the frontend. Audio data is placed into the queue for transcription.
    """
    print("Starting WebSocket-based audio listener...")
    start_audio_server(audio_queue, state)

def reauthenticate():
    login_url = Config.URL + "/login"
    uname, pw = read_creds_file()
    payload = {
        'username': uname,
        'password': pw
        }
    # print("payload", payload)
    response = requests.post(login_url, json=payload)

    if response.status_code == 200:
        print('Login successful!')
        # print('Access token:', response.json().get('access_token'))
        set_new_token(response.json().get('access_token'))
        return True
    elif response.status_code == 400:
        print('Login failed:', response.json().get('msg'))
    else:
        print('Unexpected error:', response.status_code, response.text)
    return False

def send_mic_query(query_text, token, mic_url):
    speak("Sure, let me check that for you.")
    headers = {'Authorization': f'Bearer {token}'}
    body = {'query': query_text}
    # print('mic_url', mic_url)
    # print("headers", headers)
    # print("body", body)
    # print("query_text", query_text)


    response = requests.post(mic_url, headers=headers, json=body)
    if response.status_code != 200:
        print(f"Error sending request: {response.status_code}  Response: {response.text}")
    
    if not reauthenticate():
        raise Exception("Failed to reauthenticate")
    
    token = read_token_file()
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(mic_url, headers=headers, json=body)
    if response.status_code != 200:
        print(f"Error sending request: {response.status_code}  Response: {response.text}")
        return None
    # elif response.status_code == 200:
    #     return
    

    data = response.json()
    if data['success']:
        theResponse = data['wordResponse']
        print("theResponse", theResponse)
        speak(theResponse)
    else:
        # data
        speak(data['message'])

    #     room_img_url = Config.URL + image_url

    #     def token_header(token):
    #         return {'Authorization': f'Bearer {token}'}
    #     print("room_img_url", room_img_url)
    #     response = requests.get(room_img_url, headers=token_header(token))
    #     if response.ok:
    #         # Returns bytes
    #         image_response = response.content
    #     else:
    #         print("Error get_room_img: ", response.text)
    #         image_response = None
        
    #     # Fetch the image from the image URL
    #     # image_response = requests.get(image_url, headers=headers)
    #     if response.status_code == 200:
    #         image = Image.open(BytesIO(image_response))
    #         image.show()
    #     else:
    #         print('Failed to fetch the image.')
    # else:
    #     print('Error:', data.get('text', 'Object not found'))
    
    return response.json()

def process_query(word_array):
    last_index = len(word_array) - 1
    while last_index >= 0:
        if Config.NAME_OF_VOICE_ASSISTANT.lower() in word_array[last_index]:
            frank_index = word_array[last_index].index(Config.NAME_OF_VOICE_ASSISTANT.lower()) + len(Config.NAME_OF_VOICE_ASSISTANT.lower())
            query_text = word_array[last_index][frank_index:]
            if last_index < len(word_array) - 1:
                query_text += " " + " ".join(word_array[last_index + 1:])
            return query_text.strip()
        last_index -= 1
    return None

def transcribe(audio_queue, state):
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    print("Model loaded!")
    
    word_array = []
    token = read_token_file()
    mic_url = Config.URL + "/voice_query"
    
    while True:
        if not audio_queue.empty():
            audio_chunk = audio_queue.get()
            result = model.transcribe(audio_chunk, fp16=False, language='en', no_speech_threshold=0.4)
            transcribed_text = result["text"].strip().lower()
            
            if transcribed_text:
                word_array.append(transcribed_text)
                print(f"\nTranscription: {transcribed_text}")
                
                if Config.NAME_OF_VOICE_ASSISTANT.lower() in transcribed_text:
                    state.value = State.INTAKING_QUERY.value
                    print(f"{Config.NAME_OF_VOICE_ASSISTANT.lower()} detected. Intaking query...")
            else:
                if state.value == State.INTAKING_QUERY.value:
                    query_text = process_query(word_array)
                    if query_text:
                        try:
                            response = send_mic_query(query_text, token, mic_url)
                            if response:
                                print(f"Server response: {response}")
                        except Exception as e:
                            print(f"Error sending query: {e}")
                    state.value = State.LISTENING_FOR_FRANK.value
            
            # Maintain word array size
            if len(word_array) > 1000:
                word_array = word_array[-1000:]

def main():
    audio_queue = Queue(maxsize=10)
    state = Value('i', State.LISTENING_FOR_FRANK.value)
    asyncio.run(start_audio_server(audio_queue, state))

    listen_process = Process(target=listen, args=(audio_queue, state))
    transcribe_process = Process(target=transcribe, args=(audio_queue, state))

    try:
        listen_process.start()
        transcribe_process.start()
        
        listen_process.join()
        transcribe_process.join()
    except KeyboardInterrupt:
        print("\nTerminating processes...")
        listen_process.terminate()
        transcribe_process.terminate()
    finally:
        listen_process.join()
        transcribe_process.join()

async def audio_receiver(websocket, audio_queue, state, path = None):
    """
    Receives audio data from the frontend WebSocket client
    and puts it into the audio queue for transcription.
    """
    print("Client connected for audio streaming")
    try:
        while True:
            audio_chunk = await websocket.recv()
            audio_array = np.frombuffer(audio_chunk, dtype=np.float32)

            audio_queue.put(audio_array)

            current_state = state.value
            if current_state == State.LISTENING_FOR_FRANK.value:
                state.value = State.INTAKING_QUERY.value

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected from audio stream")
    except Exception as e:
        print(f"Error in audio receiver: {e}")


import numpy as np

async def audio_handler(connection, audio_queue, state, path=None):
    print(f"New connection: {connection} with path: {path}")
    try:
        async for message in connection:
            audio_data = np.frombuffer(message, dtype=np.float32)
            audio_queue.put(audio_data)
            if state.value == State.LISTENING_FOR_FRANK.value:
                state.value = State.INTAKING_QUERY.value
    except Exception as e:
        print(f"Error in audio handler: {e}")
    finally:
        await connection.close()

async def start_audio_server(audio_queue, state):
    print("Starting WebSocket server on localhost:4001...")
    server = await websockets.serve(functools.partial(audio_handler, audio_queue=audio_queue, state=state), "localhost", 4001)
    print("WebSocket server is running. Waiting for connections...")
    await server.wait_closed()



if __name__ == "__main__":
    main()


