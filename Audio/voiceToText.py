import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

# Load your audio file
audio_file = "Recordings/recording2.wav"

# Use 'with' to open the file, which ensures the file is properly closed after processing
with sr.AudioFile(audio_file) as source:
    audio = recognizer.record(source)  # Record the audio from the file

# Convert the audio to text using Google's Web Speech API (default in SpeechRecognition)
try:
    text = recognizer.recognize_google(audio)
    print("Converted Text: ", text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio")
except sr.RequestError as e:
    print(f"Could not request results; {e}")
