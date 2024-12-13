# # # def play_text(text):
# # #     """
# # #     Takes a string and plays it through Raspberry Pi speakers.
    
# # #     Args:
# # #         text (str): The text you want to convert to speech
    
# # #     Example:
# # #         play_text("Hello, how are you?")
# # #     """
# # #     import os
# # #     from subprocess import call
    
# # #     try:
# # #         # Use espeak to convert text to speech and play it directly
# # #         call(['espeak', text])
        
# # #     except Exception as e:
# # #         print(f"Error playing audio: {str(e)}")

# # # # Example usage
# # # if __name__ == "__main__":
# # #     play_text("Testing, 1, 2, 3")

# # def play_text(text, rate=150, volume=1.0):
# #     """
# #     Takes a string and plays it through Raspberry Pi speakers using pyttsx3.
    
# #     Args:
# #         text (str): The text you want to convert to speech
# #         rate (int): Speech rate (default 150)
# #         volume (float): Volume level from 0.0 to 1.0 (default 1.0)
    
# #     Example:
# #         play_text("Hello, how are you?", rate=150, volume=0.8)
# #     """
# #     import pyttsx3
    
# #     try:
# #         # Initialize the text-to-speech engine
# #         engine = pyttsx3.init()
        
# #         # Configure the voice properties
# #         engine.setProperty('rate', rate)
# #         engine.setProperty('volume', volume)
# #         print("hi")
        
# #         # Convert text to speech and play it
# #         engine.say(text)
# #         engine.runAndWait()
        
# #     except Exception as e:
# #         print(f"Error playing audio: {str(e)}")

# # # Example usage
# # if __name__ == "__main__":
# #     play_text("Testing, 1, 2, 3")

# import pyttsx3

# def test_audio():
#     engine = pyttsx3.init()
#     # Add a print statement to see if we get here
#     print("Engine initialized")
#     # List available voices
#     voices = engine.getProperty('voices')
#     print(f"Available voices: {len(voices)}")
#     # Try to speak
#     engine.say("Test audio")
#     print("Starting speech...")
#     engine.runAndWait()
#     print("Speech complete")

# test_audio()

import pyttsx3
import logging

def play_text(text, rate=150, volume=1.0):
    """
    Takes a string and plays it through Raspberry Pi speakers using pyttsx3 with debug logging.
    """
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('pyttsx3_debug')
    
    try:
        logger.debug("Initializing pyttsx3 engine...")
        # Try different drivers
        engine = pyttsx3.init('espeak')  # Explicitly specify espeak driver
        
        logger.debug("Setting properties...")
        # Get current properties
        voices = engine.getProperty('voices')
        current_volume = engine.getProperty('volume')
        current_rate = engine.getProperty('rate')
        engine.setProperty('voice',  "com.apple.voice.compact.ru-RU.Milena")
        
        logger.debug(f"Current volume: {current_volume}")
        logger.debug(f"Current rate: {current_rate}")
        logger.debug(f"Available voices: {len(voices)}")
        
        # Set properties
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        
        logger.debug("Starting speech...")
        engine.say(text)
        
        logger.debug("Waiting for speech to complete...")
        engine.runAndWait()
        
        logger.debug("Speech completed")
        
    except Exception as e:
        logger.error(f"Error during speech: {str(e)}")
        logger.error("Try running these commands to fix dependencies:")
        logger.error("sudo apt-get update")
        logger.error("sudo apt-get install -y espeak")
        logger.error("sudo apt-get install -y python3-espeak")
        logger.error("sudo apt-get install -y alsa-utils")
        raise

# Test with different texts
if __name__ == "__main__":
    play_text("This is a test of the text to speech system.")