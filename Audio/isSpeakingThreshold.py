import sounddevice as sd
import numpy as np
import whisper
import time

# Settings
SAMPLE_RATE = 16000
KEYWORD = "start"  # The keyword to listen for
SILENCE_THRESHOLD = 0.02  # Silence detection threshold
CHUNK_DURATION = 3  # Chunk duration in seconds

def is_speaking(audio_chunk):
    """Detects if someone is speaking based on the volume."""
    volume = np.linalg.norm(audio_chunk)
    return volume > SILENCE_THRESHOLD

def transcribe_and_check_keyword(audio_data, model, keyword):
    """Transcribes audio and checks if the keyword is in the text."""
    result = model.transcribe(audio_data, fp16=False, language = "en")
    text = result["text"].strip().lower()
    print(f"Transcription: {text}")
    return keyword in text, text

def main():
    print("Loading Whisper model...")
    model = whisper.load_model("tiny")
    print("Model loaded!")

    recording_data = []
    is_keyword_detected = False

    def audio_callback(indata, frames, time, status):
        nonlocal is_keyword_detected
        if status:
            print(f"Audio status error: {status}")
        
        # Append audio data
        if is_keyword_detected or is_speaking(indata):
            recording_data.append(indata.copy())
    
    try:
        with sd.InputStream(callback=audio_callback, samplerate=SAMPLE_RATE, channels=1, dtype=np.float32):
            print("Listening for the keyword...")

            while True:
                if not is_keyword_detected:
                    # Record for a short duration
                    time.sleep(CHUNK_DURATION)
                    if recording_data:
                        audio_chunk = np.concatenate(recording_data).flatten()
                        is_keyword_detected, _ = transcribe_and_check_keyword(audio_chunk, model, KEYWORD)
                        if is_keyword_detected:
                            print(f"Keyword '{KEYWORD}' detected. Starting transcription...")
                        recording_data.clear()
                else:
                    # Continue transcription until silence is detected
                    time.sleep(CHUNK_DURATION)
                    if recording_data:
                        audio_chunk = np.concatenate(recording_data).flatten()
                        _, transcription = transcribe_and_check_keyword(audio_chunk, model, "frank")
                        print(f"Transcription: {transcription}")
                        if not is_speaking(audio_chunk):
                            print("Silence detected. Stopping transcription.")
                            is_keyword_detected = False
                    recording_data.clear()

    except KeyboardInterrupt:
        print("\nProgram terminated.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
