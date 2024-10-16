from gtts import gTTS
import os
import time


text = input("text you want to convert to speech: ")
tts = gTTS(text=text, lang='en')

audio_file = "output.mp3"
tts.save("output.mp3")

os.system("open output.mp3")  


time.sleep(5)
os.remove(audio_file)
print(f"The audio file '{audio_file}' has been deleted.")