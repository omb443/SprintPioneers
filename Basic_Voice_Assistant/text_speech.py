import pyttsx3

text_speech = pyttsx3.init()
userInput = input("Give the text to speak: ")
text_speech.say(userInput)
text_speech.runAndWait()
