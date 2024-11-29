import sounddevice as sd
import numpy as np
import whisper
import time
from multiprocessing import Queue, Process
# from enum import Enum
from enum import Enum
import requests


def main(audio_queue):
    print("Loading Whisper model...")
    print("Model loaded!")

    global the_state

    # Audio settings to match WAV format
    sample_rate = 16000
    recording_data = []
    
    def audio_callback(indata, frames, time, status):
        if status:
            print(f"Status error: {status}")
        # Normalize and append to recording buffer
        recording_data.append(indata.copy())

    try:
        with sd.InputStream(callback=audio_callback, 
                            samplerate=sample_rate,
                            channels=1,
                            dtype=np.float32):
            print("\nRecording... (Press Ctrl+C to stop)")
            
            while True:
                if the_state == State.LISTENING_FOR_FRANK or the_state == State.INTAKING_QUERY:
                    # Accumulate audio for 10 seconds
                    recording_data.clear()
                    time.sleep(2)
                    print("the shape of recording_data is: ", len(recording_data))
                    
                    if the_state == State.LISTENING:
                        print("listening")

                    if recording_data:
                        print("\nTranscribing...")
                        # Combine all audio chunks into a single array
                        audio = np.concatenate(recording_data, axis=0)
                        print("audio shpae is: ", audio.shape)
                        audio = audio.flatten()
                        audio_queue.put(audio)
                        print("audio shape after flatten: ", audio.shape)
                        
                        # Transcribe with Whisper
            

    except KeyboardInterrupt:
        print("\nRecording stopped")
    except Exception as e:
        print(f"\nError: {e}")


# make enum for state

class State(Enum):
    INTAKING_QUERY = 'listening'
    LISTENING_FOR_FRANK = 'listening for frank'
    NOT_LISTENING = 'not listening'

# state = enum('Just heard frank', 'listening', 'not listening')
the_state = State.LISTENING_FOR_FRANK
def trancribe(audio_queue):
    # if queue is not empty
    global the_state
    the_state = State.LISTENING_FOR_FRANK
    lastIndex = -1
    model = whisper.load_model("base")
    wordArray = []
    while True:
        state = False # False means not listening, True means listening
        if not audio_queue.empty():
            print("hello man ")
            audio_chunk = audio_queue.get()
            # for i in range(0, 10):
            #     result = model.transcribe(audio_chunk, fp16=False, language='en', no_speech_threshold=0.7)
            #     print(f"result {i}: ", result['text'])
            result = model.transcribe(audio_chunk, fp16=False, language='en', no_speech_threshold=0.4)
            # print("printing all segs: ")
            # print(result)
            # for segment in result['segments']:

            #     print("printing segment: ", segment)    
            #     if "alternatives" in segment:
            #         print("alternatives: ", segment["alternatives"])
            #         state = True
            #         print("Frank detected")
            #         break
            transcribed_text = result["text"].strip()
            
            if transcribed_text:
                transcribed_text = transcribed_text.lower()
                wordArray.append(transcribed_text)
                print(f"\nTranscription: {transcribed_text}")
            else:
                print("No speech detected")
                
                if the_state == State.INTAKING_QUERY:
                    # print everything said after the last frank
                    print("printing everything said after the last frank")
                      # get last instance of france in this array of strings
                    lastIndex = len(wordArray) - 1
                    lastIndexofLastIndex = -1
                    while lastIndex >= 0:
                        if "frank" in wordArray[lastIndex]:
                            # within this string where is the last index of frank
                            lastIndexofLastIndex = wordArray[lastIndex].index("frank") + len("frank")
                            break
                        else:   
                            lastIndex -= 1
                    
                    # lastIndex += 1
                print("lastIndex: ", lastIndex)
                if lastIndex >= 0 and the_state == State.INTAKING_QUERY:
                    for i in range(lastIndex, len(wordArray)):
                        if i == lastIndex:
                            print(wordArray[i][lastIndexofLastIndex:])
                        else:
                            print(wordArray[i])
                    # print(wordArray[lastIndex][lastIndexofLastIndex:])
                    the_state = State.LISTENING_FOR_FRANK
                
                # make request to the server with the query for the server to process




                    
            
            # make text lowercase
            # lower = transcribed_text.lower()
            if "frank" in transcribed_text and not state:
                the_state = State.INTAKING_QUERY
                print("Frank detected")
 
            
            
            

            # if wordArray over 1000 words remove the first words to make length 1000
            if len(wordArray) > 1000:
                wordArray = wordArray[-1000:]
            for i in range(0, len(wordArray)):
                wordArray[i] = wordArray[i].lower()

                # if the_state == state.listening:
                    # get last index - the ammount it got shifted
            
     
            
            print("\nRecording... (Press Ctrl+C to stop)")

if __name__ == "__main__":

    # Create a queue to store audio chunks that holds up to 10 items
    audio_queue = Queue(maxsize=10)

    # create multiple processes to run main and transcribe
    p1 = Process(target=main, args=(audio_queue,))
    p2 = Process(target=trancribe, args=(audio_queue,))

        # Start processes
    p1.start()
    p2.start()

    try:
        p1.join()
        p2.join()
        print("hi")
    except KeyboardInterrupt:
        print("\nTerminating processes...")
        p1.terminate()
        p2.terminate()
