# import sounddevice as sd
# import numpy as np
# import whisper
# import time
# import logging
# from multiprocessing import Queue, Process, Value
# from enum import Enum
# import requests
# from config import Config
# import os
# from PIL import Image
# from io import BytesIO
# if Config.SPEECH_ENGINE == "MAC":
#     from macSpeaker import speak
# elif Config.SPEECH_ENGINE == "GOOGLE":
#     from googlespeak import speak_text as speak
# # from googlespeak import speak_text as speak


# logging.basicConfig(
#     level=logging.INFO, 
#     format='%(message)s',
#     handlers=[ 
#         logging.FileHandler('../../webserver/app/app.log')
#         # logging.StreamHandler()         
#     ]
# )

# class State(Enum):
#     INTAKING_QUERY = 1
#     LISTENING_FOR_FRANK = 2
#     NOT_LISTENING = 3

# def read_creds_file():
#     with open(Config.CREDS_FILE_PATH, "r") as file:
#         uname = file.readline().strip()
#         pw = file.readline().strip()
#         return (uname, pw)
#     raise Exception("Failed acquiring credentials from file. Does file exist?")

# def write_token_file(new_token):
#     with open(Config.TOKEN_FILE_PATH, "w") as file:
#         file.write(new_token)


# def set_new_token(new_token):
#     write_token_file(new_token)

# def read_token_file():
#     if not os.path.exists(Config.TOKEN_FILE_PATH):
#         with open(Config.TOKEN_FILE_PATH, "w") as file:
#             file.write("")
    
#     with open(Config.TOKEN_FILE_PATH, "r") as file:
#         token = file.readline().strip()
#         return token
#     raise Exception("Failed acquiring token from file")

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

# import os
# import sys
# import ctypes
# import numpy as np
# import time
# from array import array
# import pyaudio

# # Suppress ALSA error messages
# ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int,
#                                     ctypes.c_char_p, ctypes.c_int,
#                                     ctypes.c_char_p)

# def py_error_handler(filename, line, function, err, fmt):
#     pass

# c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

# try:
#     asound = ctypes.CDLL('libasound.so.2')
#     asound.snd_lib_error_set_handler(c_error_handler)
# except:
#     pass

# def listen(audio_queue, state):
#     print("Starting audio listening process...")
    
#     # Audio configuration
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 1
#     RATE = 44100  # Using 44100 as it's more commonly supported than 16000
#     CHUNK = 1024
#     RECORD_SECONDS = 2  # Matching your original 2-second sleep
    
#     # Initialize PyAudio
#     audio = pyaudio.PyAudio()
    
#     try:
#         # Open the microphone stream
#         stream = audio.open(
#             format=FORMAT,
#             channels=CHANNELS,
#             rate=RATE,
#             input=True,
#             frames_per_buffer=CHUNK
#         )
        
#         print("\nRecording... (Press Ctrl+C to stop)")
        
#         while True:
#             current_state = state.value
#             if current_state in [State.LISTENING_FOR_FRANK.value, State.INTAKING_QUERY.value]:
#                 frames = []
                
#                 # Record for RECORD_SECONDS seconds
#                 for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#                     try:
#                         data = stream.read(CHUNK, exception_on_overflow=False)
#                         frames.append(data)
#                     except IOError as e:
#                         print(f"Warning: {e}")
#                         continue
                
#                 if frames:
#                     # Convert byte data to numpy array
#                     int_data = array('h', b''.join(frames))
#                     audio_data = np.array(int_data, dtype=np.float32) / 32768.0
#                     audio_data = audio_data.reshape(-1, 1)  # Reshape to match original format
#                     audio_queue.put(audio_data)
    
#     except KeyboardInterrupt:
#         print("\nRecording stopped")
#     except Exception as e:
#         print(f"\nError in listen process: {e}")
#     finally:
#         if 'stream' in locals():
#             stream.stop_stream()
#             stream.close()
#         audio.terminate()

# def reauthenticate():
#     login_url = Config.URL + "/login"
#     uname, pw = read_creds_file()
#     payload = {
#         'username': uname,
#         'password': pw
#         }
#     # print("payload", payload)
#     response = requests.post(login_url, json=payload)

#     if response.status_code == 200:
#         print('Login successful!')
#         # print('Access token:', response.json().get('access_token'))
#         set_new_token(response.json().get('access_token'))
#         return True
#     elif response.status_code == 400:
#         print('Login failed:', response.json().get('msg'))
#     else:
#         print('Unexpected error:', response.status_code, response.text)
#     return False

# def send_mic_query(query_text, token, mic_url):
#     speak("Sure, let me check that for you.")
#     logging.info("Sure, let me check that for you")
#     headers = {'Authorization': f'Bearer {token}'}
#     body = {'query': query_text}
#     # print('mic_url', mic_url)
#     # print("headers", headers)
#     # print("body", body)
#     # print("query_text", query_text)


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
    
#     return response.json()

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

# def transcribe(audio_queue, state):
#     print("Loading Whisper model...")
#     model = whisper.load_model("base")
#     print("Model loaded!")
    
#     word_array = []
#     token = read_token_file()
#     mic_url = Config.URL + "/voice_query"
    
#     while True:
#         if not audio_queue.empty():
#             audio_chunk = audio_queue.get()
#             result = model.transcribe(audio_chunk, fp16=False, language='en', no_speech_threshold=0.4)
#             transcribed_text = result["text"].strip().lower()
            
#             if transcribed_text:
#                 word_array.append(transcribed_text)
#                 print(f"\nTranscription: {transcribed_text}")
#                 logging.info(f"\n{transcribed_text}")
                
#                 if Config.NAME_OF_VOICE_ASSISTANT.lower() in transcribed_text:
#                     state.value = State.INTAKING_QUERY.value
#                     print(f"{Config.NAME_OF_VOICE_ASSISTANT.lower()} detected. Intaking query...")
#                     logging.info(f"{Config.NAME_OF_VOICE_ASSISTANT.lower()} detected. Intaking query...")
#             else:
#                 if state.value == State.INTAKING_QUERY.value:
#                     query_text = process_query(word_array)
#                     if query_text:
#                         try:
#                             response = send_mic_query(query_text, token, mic_url)
#                             if response:
#                                 print(f"Server response: {response}")
#                         except Exception as e:
#                             print(f"Error sending query: {e}")
#                     state.value = State.LISTENING_FOR_FRANK.value
            
#             # Maintain word array size
#             if len(word_array) > 1000:
#                 word_array = word_array[-1000:]

# def main():
#     audio_queue = Queue(maxsize=10)
#     state = Value('i', State.LISTENING_FOR_FRANK.value)
    
#     listen_process = Process(target=listen, args=(audio_queue, state))
#     # transcribe_process = Process(target=transcribe, args=(audio_queue, state))

#     try:
#         listen_process.start()
#         # transcribe_process.start()
        
#         listen_process.join()
#         # transcribe_process.join()
#     except KeyboardInterrupt:
#         print("\nTerminating processes...")
#         listen_process.terminate()
#         # transcribe_process.terminate()
#     finally:
#         listen_process.join()
#         # transcribe_process.join()


# if __name__ == "__main__":
#     main()

import os
import sys
import ctypes
import numpy as np
import whisper
import time
import logging
from multiprocessing import Queue, Process, Value
from enum import Enum
import requests
from PIL import Image
from io import BytesIO
import pyaudio
from array import array
from config import Config
from queue import Empty as QueueEmpty
import wave


if Config.SPEECH_ENGINE == "MAC":
    from macSpeaker import speak
elif Config.SPEECH_ENGINE == "GOOGLE":
    from googlespeak import speak_text as speak

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(message)s',
    handlers=[
        logging.FileHandler('../../webserver/app/app.log')
    ]
)

class State(Enum):
    INTAKING_QUERY = 1
    LISTENING_FOR_FRANK = 2
    NOT_LISTENING = 3

# ALSA error suppression
ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int,
                                    ctypes.c_char_p, ctypes.c_int,
                                    ctypes.c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

try:
    asound = ctypes.CDLL('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
except:
    pass

# ... [Previous imports and logging setup remain the same] ...

class AudioRecorder:
    def __init__(self):
        self.audio_queue = Queue(maxsize=10)
        self.state = Value('i', State.LISTENING_FOR_FRANK.value)
        self.should_stop = Value('i', 0)
        self.listen_process = None
        self.transcribe_process = None
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.RECORD_SECONDS = 2
        
    def listen(self):
        print("Starting audio listening process...")
        
        # Audio configuration

        
        # Initialize PyAudio in the child process
        audio = pyaudio.PyAudio()
        
        try:
            # Open the microphone stream
            stream = audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            
            print("\nRecording... (Press Ctrl+C to stop)")
            
            while not self.should_stop.value:
                current_state = self.state.value
                if current_state in [State.LISTENING_FOR_FRANK.value, State.INTAKING_QUERY.value]:
                    frames = []
                    
                    for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                        if self.should_stop.value:
                            break
                        try:
                            data = stream.read(self.CHUNK, exception_on_overflow=False)
                            frames.append(data)
                        except IOError as e:
                            print(f"Warning: {e}")
                            continue
                    
                    if frames:
                        # output_file = "oustput.wav"
                        # wf = wave.open(output_file, 'wb')
                        # wf.setnchannels(self.CHANNELS)
                        # wf.setsampwidth(audio.get_sample_size(self.FORMAT))
                        # wf.setframerate(self.RATE)
                        # wf.writeframes(b''.join(frames))
                        # wf.close()
                        print("done with thing")
                        # exit(0)
                        int_data = array('h', b''.join(frames))
                        audio_data = np.array(int_data, dtype=np.float32) / 32768.0
                        audio_data = audio_data.reshape(-1, 1)
                        
                        try:
                            self.audio_queue.put(audio_data, timeout=1)
                        except Queue.Full:
                            continue
        
        except Exception as e:
            print(f"\nError in listen process: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

    def transcribe(self):
        print("Loading Whisper model...")
        try:
            model = whisper.load_model("base", device="cpu")
            print("Model loaded!")
            print("\n=== Starting to Listen ===")
            print("Waiting to hear words...\n")
            
            word_array = []
            token = read_token_file()
            mic_url = Config.URL + "/voice_query"
            
            while not self.should_stop.value:
                try:
                    print("about to get something")
                    audio_chunk = self.audio_queue.get(timeout=1)
                    print("got something")
                    
                    # Ensure audio chunk is within reasonable size
                    if audio_chunk.size > 480000:
                        print("Audio chunk too large, skipping...")
                        continue
                    
                    # Convert audio to correct format for Whisper
                    audio_chunk = audio_chunk.flatten()
                    print("shape of audio is,", np.shape(audio_chunk))
                    print("audio chunk is:", audio_chunk)


                    print("getting here")
                    
                    # Use lower precision and optimize for CPU
                    result = model.transcribe(
                        audio_chunk,
                        fp16=False,
                        language='en'                    )
                    print("got a results")
                    print("result is:", result["text"])
                    
                    transcribed_text = result["text"].strip().lower()
                    
                    if transcribed_text:
                        word_array.append(transcribed_text)
                        print("\n🎤 Heard:", transcribed_text)
                        print("Current State:", "INTAKING QUERY" if self.state.value == State.INTAKING_QUERY.value else "LISTENING FOR WAKE WORD")
                        logging.info(f"\n{transcribed_text}")
                        
                        if Config.NAME_OF_VOICE_ASSISTANT.lower() in transcribed_text:
                            self.state.value = State.INTAKING_QUERY.value
                            print(f"\n🎯 Wake word detected! Listening for query...")
                            logging.info(f"{Config.NAME_OF_VOICE_ASSISTANT.lower()} detected. Intaking query...")
                    else:
                        if self.state.value == State.INTAKING_QUERY.value:
                            query_text = process_query(word_array)
                            if query_text:
                                print(f"\n📝 Processing query: {query_text}")
                                try:
                                    response = send_mic_query(query_text, token, mic_url)
                                    if response:
                                        print(f"🤖 Server response: {response}")
                                except Exception as e:
                                    print(f"❌ Error sending query: {e}")
                            self.state.value = State.LISTENING_FOR_FRANK.value
                            print("\n👂 Back to listening for wake word...")
                    
                    # Maintain word array size
                    if len(word_array) > 1000:
                        word_array = word_array[-1000:]
                        
                except QueueEmpty:
                    # Don't print anything for queue empty - it's normal operation
                    continue
                except Exception as e:
                    print(f"\n❌ Error in transcribe process: {e}")
                    time.sleep(0.1)
        
        except Exception as e:
            print(f"\n❌ Fatal error in transcribe process: {e}")
            self.should_stop.value = 1
        finally:
            # Cleanup
            del model
            import gc
            gc.collect()

    def start(self):
        """Start the recording and transcription processes"""
        self.listen_process = Process(target=self.listen)
        self.transcribe_process = Process(target=self.transcribe)
        
        self.listen_process.start()
        self.transcribe_process.start()
    
    def stop(self):
        """Stop all processes cleanly"""
        self.should_stop.value = 1
        
        if self.listen_process:
            self.listen_process.terminate()
            self.listen_process.join(timeout=1)
        
        if self.transcribe_process:
            self.transcribe_process.terminate()
            self.transcribe_process.join(timeout=1)
        
        # Clear the queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except:
                pass

# ... [Rest of the code remains the same] ...
# Helper functions
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
        set_new_token(response.json().get('access_token'))
        return True
    elif response.status_code == 400:
        print('Login failed:', response.json().get('msg'))
    else:
        print('Unexpected error:', response.status_code, response.text)
    return False

def send_mic_query(query_text, token, mic_url):
    speak("Sure, let me check that for you.")
    logging.info("Sure, let me check that for you")
    headers = {'Authorization': f'Bearer {token}'}
    body = {'query': query_text}

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

    data = response.json()
    if data['success']:
        theResponse = data['wordResponse']
        print("theResponse", theResponse)
        logging.info(theResponse)
        speak(theResponse)
    else:
        speak(data['message'])
    
    return data

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

def main():
    recorder = AudioRecorder()
    
    def signal_handler(sig, frame):
        print("\nStopping recording...")
        recorder.stop()
        sys.exit(0)
    
    import signal
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        recorder.start()
        
        # Keep the main process running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping recording...")
        recorder.stop()
    finally:
        recorder.stop()

if __name__ == "__main__":
    main()