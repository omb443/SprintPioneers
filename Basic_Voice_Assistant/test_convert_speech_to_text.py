import unittest
from unittest.mock import patch, MagicMock
import speech_recognition as sr

from voice_text import convert_speech_to_text


"""These tests check various scenarios using mocking to simulate the behavior 
of the Recognizer and Microphone classes from the SpeechRecognition library"""

class TestConvertSpeechToText(unittest.TestCase):

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')

    # test case for successful speech recognition
    def test_convert_speech_to_text_success(self, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
        mock_instance.recognize_google.return_value = "hello world"

        result = convert_speech_to_text()
        self.assertEqual(result, "hello world")

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')

    # This test checks the handling of unrecognized audio input
    def test_convert_speech_to_text_empty_audio(self, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
        mock_instance.recognize_google.side_effect = sr.UnknownValueError()

        result = convert_speech_to_text()
        self.assertEqual(result, "Sorry, I could not understand the audio.")

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')
    def test_convert_speech_to_text_silence(self, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
     
        mock_instance.recognize_google.side_effect = sr.UnknownValueError()

        result = convert_speech_to_text()
        self.assertEqual(result, "Sorry, I could not understand the audio.")

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')

    
    # test case to check function handing request error
    def test_convert_speech_to_text_request_error(self, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
        mock_instance.recognize_google.side_effect = sr.RequestError()

        result = convert_speech_to_text()
        self.assertEqual(result, "Could not request results from Google Speech Recognition service.")



if __name__ == '__main__':
    unittest.main()
