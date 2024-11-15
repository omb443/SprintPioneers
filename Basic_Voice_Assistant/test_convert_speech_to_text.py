import unittest
from unittest.mock import patch, MagicMock
import speech_recognition as sr

from voice_text import convert_speech_to_text


class TestConvertSpeechToText(unittest.TestCase):

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')
    @patch('voice_text.emotion_detection.predict')
    def test_convert_speech_to_text_success(self, mock_predict, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
        mock_instance.recognize_google.return_value = "hello world"
        
      
        mock_predict.return_value = "neutral"

        result = convert_speech_to_text()
        self.assertEqual(result, "hello world")

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')
    @patch('voice_text.emotion_detection.predict')
    def test_convert_speech_to_text_empty_audio(self, mock_predict, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
        mock_instance.recognize_google.side_effect = sr.UnknownValueError()
        
        
        mock_predict.return_value = "neutral"

        result = convert_speech_to_text()
        self.assertEqual(result, "Sorry, I could not understand the audio.")

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')
    @patch('voice_text.emotion_detection.predict')
    def test_convert_speech_to_text_silence(self, mock_predict, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
        mock_instance.recognize_google.side_effect = sr.UnknownValueError()
        
       
        mock_predict.return_value = "neutral"

        result = convert_speech_to_text()
        self.assertEqual(result, "Sorry, I could not understand the audio.")

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')
    @patch('voice_text.emotion_detection.predict')
    def test_convert_speech_to_text_request_error(self, mock_predict, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
        mock_instance.recognize_google.side_effect = sr.RequestError()
        
       
        mock_predict.return_value = "neutral"

        result = convert_speech_to_text()
        self.assertEqual(result, "Could not request results from Google Speech Recognition service.")


if __name__ == '__main__':
    unittest.main()
