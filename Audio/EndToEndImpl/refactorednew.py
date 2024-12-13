# # import sounddevice as sd
# # import numpy as np
# # import whisper
# # import time
# # import logging
# # from multiprocessing import Queue, Process, Value
# # from enum import Enum
# # import requests
# # from config import Config
# # import os
# # from PIL import Image
# # from io import BytesIO
# # if Config.SPEECH_ENGINE == "MAC":
# #     from macSpeaker import speak
# # elif Config.SPEECH_ENGINE == "GOOGLE":
# # from googlespeak import speak_text as speak
# # # from googlespeak import speak_text as speak


import sys


import sounddevice as sd
import numpy as np
import whisper
import time
import logging
from multiprocessing import Queue, Process, Value, Event
from enum import Enum
import requests
from config import Config
import os
from PIL import Image
from io import BytesIO

if Config.SPEECH_ENGINE == "MAC":
    from macSpeaker import speak
elif Config.SPEECH_ENGINE == "GOOGLE":
    from googlespeak import speak_text as speak




# # logging.basicConfig(
# #     level=logging.INFO, 
# #     format='%(message)s',
# #     handlers=[ 
# #         logging.FileHandler('../../webserver/app/app.log')
# #         # logging.StreamHandler()         
# #     ]
# # )

# # class State(Enum):
# #     INTAKING_QUERY = 1
# #     LISTENING_FOR_FRANK = 2
# #     NOT_LISTENING = 3

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

# # def listen(audio_queue, state):
# #     print("Starting audio listening process...")
# #     # logging.info("Starting audio listening process...")
# #     sample_rate = 16000
# #     recording_data = []
    
# #     def audio_callback(indata, frames, time, status):
# #         recording_data.append(indata.copy())

# #     try:
# #         with sd.InputStream(callback=audio_callback, 
# #                           samplerate=sample_rate,
# #                           channels=1,
# #                           dtype=np.float32):
# #             print("\nRecording... (Press Ctrl+C to stop)")
# #             # logging.info("\nRecording... (Press Ctrl+C to stop)")
            
# #             while True:
# #                 current_state = state.value
# #                 if current_state in [State.LISTENING_FOR_FRANK.value, State.INTAKING_QUERY.value]:
# #                     recording_data.clear()
# #                     time.sleep(2)
                    
# #                     # if current_state == State.INTAKING_QUERY.value:
# #                     #     print("listening")

# #                     if recording_data:
# #                         # print("\nProcessing audio chunk...")
# #                         audio = np.concatenate(recording_data, axis=0)
# #                         audio = audio.flatten()
# #                         audio_queue.put(audio)

# #     except KeyboardInterrupt:
# #         print("\nRecording stopped")
# #     except Exception as e:
# #         print(f"\nError in listen process: {e}")

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

# def send_mic_query(query_text, token, mic_url):
#     speak("Sure, let me check that for you.")
#     logging.info("Sure, let me check that for you")
#     headers = {'Authorization': f'Bearer {token}'}
#     body = {'query': query_text}
#     print('mic_url', mic_url)
#     print("headers", headers)
#     print("body", body)
#     print("query_text", query_text)


#     response = requests.post(mic_url, headers=headers, json=body)
#     if response.status_code != 200:
#         print(f"Error sending request: {response.status_code}  Response: {response.text}")
#         if not reauthenticate():
#             raise Exception("Failed to reauthenticate")
    
#         token = read_token_file()
        
#         headers = {'Authorization': f'Bearer {token}'}
#         response = requests.post(mic_url, headers=headers, json=body)
#         if response.status_code != 200:
#             print(f"Error sending request: {response.status_code}  Response: {response.text}")
#             return None
#     # elif response.status_code == 200:
#     #     return
    

#     data = response.json()
#     if data['success']:
#         theResponse = data['wordResponse']
#         print("theResponse", theResponse)
#         logging.info(theResponse)
#         speak(theResponse)
#     else:
#         # data
#         speak(data['message'])



# def send_transcribe_query(npArray, token, transcribe_url):
#     print("halo")
#     speak("Sure, let me check that for you.")
#     print("hey")
#     logging.info("Sure, let me check that for you")
#     headers = {'Authorization': f'Bearer {token}'}
#     body = {'list': npArray.toList()}
#     print('transcribe url', transcribe_url)
#     print("headers", headers)
#     print("body", body)
#     # print("query_text", )


#     response = requests.post(transcribe_url, headers=headers, json=body)
#     print("actual send")
#     if response.status_code != 200:
#         print(f"Error sending request: {response.status_code}  Response: {response.text}")
#         if not reauthenticate():
#             raise Exception("Failed to reauthenticate")
    
#         token = read_token_file()
        
#         headers = {'Authorization': f'Bearer {token}'}
#         response = requests.post(transcribe_url, headers=headers, json=body)
#         if response.status_code != 200:
#             print(f"Error sending request: {response.status_code}  Response: {response.text}")
#             return None
#     # elif response.status_code == 200:
#     #     return
#     print("am here")

#     data = response.json()

#     # if data['success']:
#     #     theResponse = data['wordResponse']
#     #     print("theResponse", theResponse)
#     #     logging.info(theResponse)
#     #     speak(theResponse)
#     # else:
#     #     # data
#     #     speak(data['message'])
#     return data['text']
        

#     #     room_img_url = Config.URL + image_url

#     #     def token_header(token):
#     #         return {'Authorization': f'Bearer {token}'}
#     #     print("room_img_url", room_img_url)
#     #     response = requests.get(room_img_url, headers=token_header(token))
#     #     if response.ok:
#     #         # Returns bytes
#     #         image_response = response.content
#     #     else:
#     #         print("Error get_room_img: ", response.text)
#     #         image_response = None
        
#     #     # Fetch the image from the image URL
#     #     # image_response = requests.get(image_url, headers=headers)
#     #     if response.status_code == 200:
#     #         image = Image.open(BytesIO(image_response))
#     #         image.show()
#     #     else:
#     #         print('Failed to fetch the image.')
#     # else:
#     #     print('Error:', data.get('text', 'Object not found'))
    
#     # return response.json()

# def process_query(word_array):
#     last_index = len(word_array) - 1
#     while last_index >= 0:
#         if Config.NAME_OF_VOICE_ASSISTANT.lower() in word_array[last_index]:
#             frank_index = word_array[last_index].index(Config.NAME_OF_VOICE_ASSISTANT.lower()) + len(Config.NAME_OF_VOICE_ASSISTANT.lower())
#             query_text = word_array[last_index][frank_index:]
#             if last_index < len(word_array) - 1:
#                 query_text += " " + " ".join(word_array[last_index + 1:])
#             return query_text.strip()
#         last_index -= 1
#     return None

# # def transcribe(audio_queue, state):
# #     print("Loading Whisper model...")
# #     model = whisper.load_model("base")
# #     print("Model loaded!")
    
# #     word_array = []
# #     token = read_token_file()
# #     mic_url = Config.URL + "/voice_query"
    
# #     while True:
# #         if not audio_queue.empty():
# #             audio_chunk = audio_queue.get()
# #             result = model.transcribe(audio_chunk, fp16=False, language='en', no_speech_threshold=0.4)
# #             transcribed_text = result["text"].strip().lower()
            
# #             if transcribed_text:
# #                 word_array.append(transcribed_text)
# #                 print(f"\nTranscription: {transcribed_text}")
# #                 logging.info(f"\n{transcribed_text}")
                
# #                 if Config.NAME_OF_VOICE_ASSISTANT.lower() in transcribed_text:
# #                     state.value = State.INTAKING_QUERY.value
# #                     print(f"{Config.NAME_OF_VOICE_ASSISTANT.lower()} detected. Intaking query...")
# #                     logging.info(f"{Config.NAME_OF_VOICE_ASSISTANT.lower()} detected. Intaking query...")
# #             else:
# #                 if state.value == State.INTAKING_QUERY.value:
# #                     query_text = process_query(word_array)
# #                     if query_text:
# #                         try:
# #                             response = send_mic_query(query_text, token, mic_url)
# #                             if response:
# #                                 print(f"Server response: {response}")
# #                         except Exception as e:
# #                             print(f"Error sending query: {e}")
# #                     state.value = State.LISTENING_FOR_FRANK.value
            
# #             # Maintain word array size
# #             if len(word_array) > 1000:
# #                 word_array = word_array[-1000:]

# # def main():
# #     audio_queue = Queue(maxsize=10)
# #     state = Value('i', State.LISTENING_FOR_FRANK.value)
    
# #     listen_process = Process(target=listespeak(
# #         listen_process.join()
# #         transcribe_process.join()


# # if __name__ == "__main__":
# #     main()



# logging.basicConfig(
#     level=logging.INFO,
#     format='%(message)s',
#     handlers=[
#         logging.FileHandler('../../webserver/app/app.log')
#     ]
# )

# class State(Enum):
#     INTAKING_QUERY = 1
#     LISTENING_FOR_FRANK = 2
#     NOT_LISTENING = 3

# def audio_callback(indata, frames, time, status, audio_queue):
#     """Callback function to handle audio data"""
#     if status:
#         print(f'Audio callback status: {status}')
#     audio_queue.put(indata.copy())

# def listen_and_buffer(audio_queue, state, stop_event):
#     """Main audio capture function running in the main process"""
#     print("Starting audio listening process...")
#     sample_rate = 16000
    
#     try:
#         with sd.InputStream(callback=lambda *args: audio_callback(*args, audio_queue),
#                           samplerate=sample_rate,
#                           channels=1,
#                           dtype=np.float32,
#                           blocksize=8000):  # Adjust blocksize as needed
#             while not stop_event.is_set():
#                 time.sleep(0.1)  # Prevent busy waiting
                
#     except Exception as e:
#         print(f"Error in audio capture: {e}")
#         return

# def process_audio(audio_queue, state, stop_event):
#     """Process audio data in a separate process"""
#     print("Loading Whisper model...")
#     # model = whisper.load_model("tiny")
#     print("Model loaded!")
    
#     word_array = []
#     token = read_token_file()
#     mic_url = Config.URL + "/voice_query"
#     transcribe_url = Config.URL + "/transcribe"
    
#     audio_buffer = []
    
#     while not stop_event.is_set():
#         if not audio_queue.empty():
#             try:
#                 audio_chunk = audio_queue.get_nowait()
#                 # print("type of audiochunk is", np.shape(audio_chunk))
#                 audio_buffer.append(audio_chunk)
#                 # print("is it here?")
#                 # print(len(audio_buffer))
#                 # Process accumulated audio every 2 seconds
#                 if len(audio_buffer) >= 5:  # Adjust this value based on your blocksize
#                     # print("longer")
#                     audio_data = np.concatenate(audio_buffer, axis=0)
#                     # print("just concattinated")
#                     # print("shape", np.shape(audio_data))
#                     audio_data = audio_data.flatten()
#                     # print("aftr flatten", np.shape(audio_data))
#                     audio_buffer = []
#                     print("boutta send")
#                     # result = model.transcribe(audio_data, fp16=False, language='en', no_speech_threshold=0.4)
#                     transcribed_text  = send_transcribe_query(audio_data, token, transcribe_url)
#                     # print("past ranscirbe")
#                     # transcribed_text = result["text"].strip().lower()
                    
#                     if transcribed_text:
#                         word_array.append(transcribed_text)
#                         print(f"\nTranscription: {transcribed_text}")
#                         logging.info(f"\n{transcribed_text}")
                        
#                         if Config.NAME_OF_VOICE_ASSISTANT.lower() in transcribed_text:
#                             state.value = State.INTAKING_QUERY.value
#                             print(f"{Config.NAME_OF_VOICE_ASSISTANT.lower()} detected. Intaking query...")
#                             logging.info(f"{Config.NAME_OF_VOICE_ASSISTANT.lower()} detected. Intaking query...")
#                         else:
#                             if state.value == State.INTAKING_QUERY.value:
#                                 query_text = process_query(word_array)
#                                 if query_text:
#                                     try:
#                                         response = send_mic_query(query_text, token, mic_url)
#                                         if response:
#                                             print(f"Server response: {response}")
#                                     except Exception as e:
#                                         print(f"Error sending query: {e}")
#                                     state.value = State.LISTENING_FOR_FRANK.value
                        
#                         # Maintain word array size
#                         if len(word_array) > 1000:
#                             word_array = word_array[-1000:]
                            
#             except Exception as e:
#                 print(f"Error processing audio: {e}")

# def main():
#     audio_queue = Queue()
#     state = Value('i', State.LISTENING_FOR_FRANK.value)
#     stop_event = Event()
    
#     # Create the processing process
#     process_process = Process(target=process_audio, args=(audio_queue, state, stop_event))
    
#     try:
#         # Start the processing process
#         process_process.start()
        
#         # Run audio capture in the main process
#         listen_and_buffer(audio_queue, state, stop_event)
        
#     except KeyboardInterrupt:
#         print("\nTerminating...")
#         stop_event.set()
        
#     finally:
#         stop_event.set()
#         process_process.join()
#         print("Cleanup complete")

# if __name__ == "__main__":
#     main()

# # Keep your existing helper functions (read_creds_file, write_token_file, etc.) as they are

import sounddevice as sd
import numpy as np
import time
import logging
from collections import deque
from config import Config
import requests
from enum import Enum
import os

class State(Enum):
    INTAKING_QUERY = 1
    LISTENING_FOR_FRANK = 2
    NOT_LISTENING = 3

# class AudioHandler:
#     def __init__(self):
#         self.sample_rate = 16000
#         self.audio_buffer = deque(maxlen=5)  # Adjust buffer size as needed
#         self.word_array = []
#         self.token = read_token_file()
#         self.mic_url = Config.URL + "/voice_query"
#         self.transcribe_url = Config.URL + "/transcribe"
#         self.state = State.LISTENING_FOR_FRANK
#         self.is_running = True

#         self.stream = sd.InputStream(
#         callback=self.audio_callback,
#         samplerate=self.sample_rate,
#         channels=1,
#         dtype=np.float32,
#         blocksize=32000
#         )

#     def audio_callback(self, indata, frames, time, status):
#         """Callback to handle incoming audio data"""
#         if status:
#             print(f'Audio callback status: {status}')
#         # sys.stdout.write("in call back\r")
#         # sys.stdout.flush()
#         # print("hello its a me", end='\r\n', flush=True)        # print("calling callback")
#         # print("inddeed so", end='\r\n', flush=True)
#         # print("suciety", end='\r\n', flush=True)
#         # Add new audio data to buffer
#         print(np.shape(indata))
#         if self.state != State.NOT_LISTENING:
#             self.audio_buffer.append(indata.copy())
        
#         # Process buffer when it reaches certain size
#         if len(self.audio_buffer) >= 2:
#             self.process_audio_buffer()

#     def process_audio_buffer(self):
#         """Process accumulated audio data"""
#         try:
#             # Concatenate and flatten audio data
#             audio_data = np.concatenate(self.audio_buffer, axis=0)
#             audio_data = audio_data.flatten()
            
#             # Clear buffer after processing
#             self.audio_buffer.clear()
#             # model = whisper.load_model("tiny")
#             # result = model.transcribe(audio_data, fp16=False, language='en', no_speech_threshold=0.4)
#             # transcribed_text = result["text"].strip().lower()
#             # print("just processed", transcribed_text)
            
#             # Send for transcription
#             #time before
#             before = time.time()
#             transcribed_text = self.send_transcribe_query(audio_data)
#             after = time.time() - before
#             print(after)
            
#             if transcribed_text:
#                 self.word_array.append(transcribed_text)
#                 print(f"\nTranscription: {transcribed_text}")
#                 logging.info(f"\n{transcribed_text}")
                
#                 if Config.NAME_OF_VOICE_ASSISTANT.lower() in transcribed_text:
#                     self.state = State.INTAKING_QUERY
#                     print(f"{Config.NAME_OF_VOICE_ASSISTANT.lower()} detected. Intaking query...")
#                     logging.info(f"{Config.NAME_OF_VOICE_ASSISTANT.lower()} detected. Intaking query...")
#                 else:
#                     if self.state == State.INTAKING_QUERY:
#                         query_text = self.process_query()
#                         if query_text:
#                             self.state = State.NOT_LISTENING
#                             self.handle_query(query_text)
#                             self.state = State.LISTENING_FOR_FRANK

#                 # Maintain word array size
#                 if len(self.word_array) > 1000:
#                     self.word_array = self.word_array[-1000:]
#             else:
#                 if self.state == State.INTAKING_QUERY:
#                     query_text = self.process_query()
#                     if query_text:
#                         self.state = State.NOT_LISTENING
#                         self.handle_query(query_text)
#                         self.state = State.LISTENING_FOR_FRANK
#                         afterafteer = time.time()
#                         print("full time is: ", (afterafteer - before))
#         except Exception as e:
#             print(f"Error processing audio: {e}")

#     def send_transcribe_query(self, audio_data):
#         # speak("Sure, let me check that for you.")
#         logging.info("Sure, let me check that for you")
#         # print("self token is", self.token)
#         headers = {'Authorization': f'Bearer {self.token}'}

#         body = {'list': audio_data.tolist()}
#         # print("About to send header: ", headers)
#         response = requests.post(self.transcribe_url, headers=headers, json=body)
        
#         if response.status_code != 200:
#             if reauthenticate():
#                 self.token = read_token_file()
#                 headers = {'Authorization': f'Bearer {self.token}'}
#                 response = requests.post(self.transcribe_url, headers=headers, json=body)
#                 if response.status_code != 200:
#                     return None
#             else:
#                 return None
        
#         data = response.json()
#         return data['text']

#     def handle_query(self, query_text):
#         """Handle processing of recognized query"""
#         print("self token is", self.token)
#         print("query text is:", query_text)
#         try:
#             speak("Sure, let me check that for you.")
#             headers = {'Authorization': f'Bearer {self.token}'}
#             body = {'query': query_text}
#             print("query_text", query_text)
            
#             print("About to send header: ", headers)
#             response = requests.post(self.mic_url, headers=headers, json=body)
            
#             if response.status_code != 200:
#                 if reauthenticate():
#                     self.token = read_token_file()
#                     headers = {'Authorization': f'Bearer {self.token}'}
#                     response = requests.post(self.mic_url, headers=headers, json=body)
                    
#             data = response.json()
#             if data['success']:
#                 theResponse = data['wordResponse']
#                 print("theResponse", theResponse)
#                 logging.info(theResponse)
#                 speak(theResponse)
#             else:
#                 speak(data['message'])
                
#         except Exception as e:
#             print(f"Error handling query: {e}")

#     def process_query(self):
#         """Process word array to extract query"""
#         last_index = len(self.word_array) - 1
#         while last_index >= 0:
#             if Config.NAME_OF_VOICE_ASSISTANT.lower() in self.word_array[last_index]:
#                 frank_index = self.word_array[last_index].index(Config.NAME_OF_VOICE_ASSISTANT.lower()) + len(Config.NAME_OF_VOICE_ASSISTANT.lower())
#                 query_text = self.word_array[last_index][frank_index:]
#                 if last_index < len(self.word_array) - 1:
#                     query_text += " " + " ".join(self.word_array[last_index + 1:])
#                 return query_text.strip()
#             last_index -= 1
#         return None

#     def start(self):
#         """Start the audio processing"""
#         with self.stream:
#             print("Recording started...")
#             while self.is_running:
#                 time.sleep(0.1)  # Prev

import threading

class AudioHandler:
    def __init__(self):
        self.sample_rate = 16000
        self.audio_buffer = deque(maxlen=5)
        self.word_array = []
        self.token = read_token_file()
        self.mic_url = Config.URL + "/voice_query"
        self.transcribe_url = Config.URL + "/transcribe"
        self.state = State.LISTENING_FOR_FRANK
        self.is_running = True
        self.is_handling_query = False

        self.stream = sd.InputStream(
            callback=self.audio_callback,
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32,
            blocksize=48000
        )
    def send_transcribe_query(self, audio_data):
        # speak("Sure, let me check that for you.")
        logging.info("Sure, let me check that for you")
        # print("self token is", self.token)
        headers = {'Authorization': f'Bearer {self.token}'}

        body = {'list': audio_data.tolist()}
        # print("About to send header: ", headers)
        response = requests.post(self.transcribe_url, headers=headers, json=body)
        
        if response.status_code != 200:
            if reauthenticate():
                self.token = read_token_file()
                headers = {'Authorization': f'Bearer {self.token}'}
                response = requests.post(self.transcribe_url, headers=headers, json=body)
                if response.status_code != 200:
                    return None
            else:
                return None
        
        data = response.json()
        return data['text']
    
    def process_query(self):
        """Process word array to extract query"""
        last_index = len(self.word_array) - 1
        while last_index >= 0:
            if Config.NAME_OF_VOICE_ASSISTANT.lower() in self.word_array[last_index]:
                frank_index = self.word_array[last_index].index(Config.NAME_OF_VOICE_ASSISTANT.lower()) + len(Config.NAME_OF_VOICE_ASSISTANT.lower())
                query_text = self.word_array[last_index][frank_index:]
                if last_index < len(self.word_array) - 1:
                    query_text += " " + " ".join(self.word_array[last_index + 1:])
                return query_text.strip()
            last_index -= 1
        return None

    def audio_callback(self, indata, frames, time, status):
        """Callback to handle incoming audio data"""
        if status:
            print(f'Audio callback status: {status}', flush=True)
        
        print(".", end="", flush=True)  # Visual indicator that callback is running
        
        # Only process audio if we're not handling a query and not in NOT_LISTENING state
        if not self.is_handling_query and self.state != State.NOT_LISTENING:
            self.audio_buffer.append(indata.copy())
            
            # Process buffer when it reaches certain size
            if len(self.audio_buffer) >= 2:
                # Start processing in a separate thread to avoid blocking the callback
                process_thread = threading.Thread(target=self.process_audio_buffer)
                process_thread.start()

    def process_audio_buffer(self):
        """Process accumulated audio data"""
        try:
            # Make a copy of the buffer and clear it
            buffer_copy = list(self.audio_buffer)
            self.audio_buffer.clear()
            print("hi")
            # Process the copy
            audio_data = np.concatenate(buffer_copy, axis=0)
            audio_data = audio_data.flatten()
            
            before = time.time()
            transcribed_text = self.send_transcribe_query(audio_data)
            after = time.time() - before
            print(f"\nTranscription time: {after}", flush=True)
            
            if transcribed_text:
                self.word_array.append(transcribed_text)
                print(f"\nTranscription: {transcribed_text}", flush=True)
                logging.info(f"\n{transcribed_text}")
                
                if Config.NAME_OF_VOICE_ASSISTANT.lower() in transcribed_text:
                    self.state = State.INTAKING_QUERY
                    print(f"\n{Config.NAME_OF_VOICE_ASSISTANT.lower()} detected. Intaking query...", flush=True)
                    logging.info(f"{Config.NAME_OF_VOICE_ASSISTANT.lower()} detected. Intaking query...")
                else:
                    if self.state == State.INTAKING_QUERY:
                        query_text = self.process_query()
                        if query_text:
                            # Handle query in a separate thread
                            query_thread = threading.Thread(target=self._handle_query, args=(query_text,))
                            query_thread.start()

        except Exception as e:
            print(f"\nError processing audio: {e}", flush=True)

    def _handle_query(self, query_text):
        """Internal method to handle query in a separate thread"""
        try:
            self.is_handling_query = True
            self.state = State.NOT_LISTENING
            
            print("\nHandling query:", query_text, flush=True)
            speak("Sure, let me check that for you.")
            
            headers = {'Authorization': f'Bearer {self.token}'}
            body = {'query': query_text}
            
            response = requests.post(self.mic_url, headers=headers, json=body)
            
            if response.status_code != 200:
                if reauthenticate():
                    self.token = read_token_file()
                    headers = {'Authorization': f'Bearer {self.token}'}
                    response = requests.post(self.mic_url, headers=headers, json=body)
            
            data = response.json()
            if data['success']:
                theResponse = data['wordResponse']
                print("\nResponse:", theResponse, flush=True)
                logging.info(theResponse)
                speak(theResponse)
            else:
                speak(data['message'])
                
        except Exception as e:
            print(f"\nError handling query: {e}", flush=True)
        finally:
            self.is_handling_query = False
            self.state = State.LISTENING_FOR_FRANK

    def start(self):
        """Start the audio processing"""
        with self.stream:
            print("Recording started...", flush=True)
            while self.is_running:
                time.sleep(0.1)

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.FileHandler('../../webserver/app/app.log')
        ]
    )
    
    handler = AudioHandler()
    try:
        handler.start()
    except KeyboardInterrupt:
        print("\nStopping...")
        handler.is_running = False

if __name__ == "__main__":
    main()