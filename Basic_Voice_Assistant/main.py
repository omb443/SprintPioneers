import voice_text
import basic_llm
import text_speech

def main():
    content = voice_text.convert_speech_to_text()
    text = basic_llm.get_respose(content)
    text_speech.to_speech(text)


main()
