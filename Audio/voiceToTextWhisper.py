import whisper

# Load the pre-trained Whisper model
model = whisper.load_model("base")

# Transcribe the audio file
result = model.transcribe("Recordings/recording2.wav")

# Print the recognized text
print(result['text'])
