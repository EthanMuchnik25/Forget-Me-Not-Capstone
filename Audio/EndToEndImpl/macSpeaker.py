import pyttsx3

def speak(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set the output device to the Mac's built-in speaker (optional)
    engine.setProperty('volume', 1.0)  # Max volume
<<<<<<< HEAD

=======
    engine.setProperty('voice', "com.apple.voice.compact.ru-RU.Milena")

    # com.apple.speech.synthesis.voice.GoodNews
>>>>>>> ccbb3579298f9701f119b948cdd104aa2efc9120
    # # Set the text to speak
    # text = "Hello, this is a voice response from your Mac!"

    # Speak the text
    engine.say(text)
    engine.runAndWait()

<<<<<<< HEAD
=======
if __name__ == "__main__":
    # Test with a simple message
    speak("Hello! This is a test of text to speech.")
    
    # Test with a longer message
    speak("You can convert any text to speech using this function. It supports multiple languages too!")
    
    # Test with a different language (French)
    speak("Bonjour! Comment allez-vous?")

>>>>>>> ccbb3579298f9701f119b948cdd104aa2efc9120
