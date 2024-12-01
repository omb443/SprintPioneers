import google.generativeai as genai
import voice_text

#  Put your own key here
GOOGLE_API_KEY= '' 
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

def get_respose(content):

    response = model.generate_content(content)

    return(response._result.candidates[0].content.parts[0].text)
