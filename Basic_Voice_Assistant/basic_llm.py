!pip install google-generativeai


import google.generativeai as genai
import voice_text

GOOGLE_API_KEY= 'AIzaSyC7-H1L5u7YCAYUYiRaCA6rCheATuu2JoI'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

context = voice_text.convert_speech_to_text()

response = model.generate_content(context)

print(response._result.candidates[0].content.parts[0].text)
