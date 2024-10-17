import pyttsx3

def to_speech(text):
    text_speech = pyttsx3.init()
    text_speech.say(text)
    text_speech.runAndWait()
