from gtts import gTTS
import pygame
import os
import tempfile
import time

def speak_text(text, lang='en'):
    """
    Convert text to speech and play it immediately using pygame
    
    Args:
        text (str): The text to convert to speech
        lang (str): Language code (default: 'en' for English)
    """
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        temp_filename = fp.name
        
    # Convert text to speech
    tts = gTTS(text=text, lang=lang, slow=False)
    
    # Save to temporary file
    tts.save(temp_filename)
    
    # Load and play the audio
    pygame.mixer.music.load(temp_filename)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    # Clean up
    pygame.mixer.music.unload()
    pygame.mixer.quit()
    os.remove(temp_filename)

# Example usage
if __name__ == "__main__":
    # Test with a simple message
    speak_text("Hello! This is a test of text to speech.")
    
    # Test with a longer message
    speak_text("You can convert any text to speech using this function. It supports multiple languages too!")
    
    # Test with a different language (French)
    speak_text("Bonjour! Comment allez-vous?", lang='fr')