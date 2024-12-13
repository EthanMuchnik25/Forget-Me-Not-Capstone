from multiprocessing import Queue, Value, Process, Lock
import sounddevice as sd
import numpy as np
import whisper
import time

SAMPLE_RATE = 16000
CHUNK_DURATION = 3  # seconds

def audio_capture(audio_queue, queue_counter, lock):
    def audio_callback(indata, frames, time, status):
        if status:
            print(f"Audio status error: {status}")
        # Add audio chunk to queue
        if not audio_queue.full():
            audio_queue.put(indata.copy())
            with lock:  # Safely update the counter
                queue_counter.value += 1

    with sd.InputStream(callback=audio_callback, samplerate=SAMPLE_RATE, channels=1, dtype=np.float32):
        print("Recording... (Press Ctrl+C to stop)")
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nStopping audio capture process.")

def transcribe_audio(audio_queue, queue_counter, lock, model):
    try:
        while True:
            if not audio_queue.empty():
                # Remove audio chunk from the queue
                audio_chunk = audio_queue.get()
                with lock:  # Safely update the counter
                    queue_counter.value -= 1

                print(f"Transcribing... Remaining items in queue: {queue_counter.value}")

                # Flatten and normalize the audio
                audio = audio_chunk.flatten()
                audio = audio / np.max(np.abs(audio))

                # Transcribe the audio
                result = model.transcribe(audio, fp16=False)
                transcribed_text = result["text"].strip()
                print(f"Transcription: {transcribed_text}")
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping transcription process.")

if __name__ == "__main__":
    # Load Whisper model
    print("Loading Whisper model...")
    model = whisper.load_model("tiny")
    print("Model loaded!")

    # Shared resources
    audio_queue = Queue(maxsize=5)
    queue_counter = Value('i', 0)  # Shared counter (integer)
    lock = Lock()  # Lock for thread-safe counter updates

    # Create processes
    audio_process = Process(target=audio_capture, args=(audio_queue, queue_counter, lock))
    transcription_process = Process(target=transcribe_audio, args=(audio_queue, queue_counter, lock, model))

    # Start processes
    audio_process.start()
    transcription_process.start()

    try:
        audio_process.join()
        transcription_process.join()
    except KeyboardInterrupt:
        print("\nTerminating processes...")
        audio_process.terminate()
        transcription_process.termi
