import pyttsx3

def speak(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set the output device to the Mac's built-in speaker (optional)
    engine.setProperty('volume', 1.0)  # Max volume

    # # Set the text to speak
    # text = "Hello, this is a voice response from your Mac!"

    # Speak the text
    engine.say(text)
    engine.runAndWait()

