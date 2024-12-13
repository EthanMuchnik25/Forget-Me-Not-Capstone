import ctypes

# Suppress ALSA error messages
# NOTE: This must be done before importing pyaudio
ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int,
                                    ctypes.c_char_p, ctypes.c_int,
                                    ctypes.c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = ctypes.CDLL('libasound.so.2')
asound.snd_lib_error_set_handler(c_error_handler)

# Now import pyaudio
import pyaudio
import wave

# Configuration
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1  # Mono
RATE = 44100  # Sampling rate in Hz
CHUNK = 1024  # Number of frames per buffer
RECORD_SECONDS = 5  # Duration of recording

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the microphone stream
stream = audio.open(format=FORMAT, 
                   channels=CHANNELS,
                   rate=RATE, 
                   input=True,
                   frames_per_buffer=CHUNK)

print("Recording...")
frames = []

# Record audio
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording finished.")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recording to a file
output_file = "output.wav"
wf = wave.open(output_file, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"Audio recorded and saved to {output_file}")