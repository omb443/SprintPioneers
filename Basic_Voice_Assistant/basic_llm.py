import google.generativeai as genai
import voice_text

GOOGLE_API_KEY= 'AIzaSyC7-H1L5u7YCAYUYiRaCA6rCheATuu2JoI'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

def get_respose(content):

    response = model.generate_content(content)

    return(response._result.candidates[0].content.parts[0].text)
