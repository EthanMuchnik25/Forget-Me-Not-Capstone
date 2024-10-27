import pyttsx3

engine = pyttsx3.init()

engine.setProperty('rate', 150)
engine.setProperty('volume', 1) #rante 0.0 to 1.0

def speak(text):
  """ Function to make the assistant speak """
  engine.say(text)
  engine.runAndWait() # Don't want to block

