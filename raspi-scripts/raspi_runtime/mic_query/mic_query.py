import speech_recognition as sr
from config import Config
if Config.MOCK_SPEAKER:
    from mocks.speak_txt import speak
else:
    from speak_txt import speak


# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()


# TODO eventually, this should be mocked out. However, I do not know enough 
#  about how this works to mock it out. Test it once people are awake
def listen_for_activation():
    """ Function to listen for the activation phrase "Blue egg" """
    with sr.Microphone() as source:
        print("Listening for the activation phrase...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

        try:
            # Convert audio to text
            text = recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")

            # Check if the activation phrase is spoken
            if "blue egg" in text:
                speak("How can I assist you?")
                print("Activation phrase detected!")
                # Here you can add further functionality after activation
                # TODO not difficult to send query to server
            else:
                print("Activation phrase not detected.")

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")

if __name__ == "__main__":
    while True:
        listen_for_activation()
