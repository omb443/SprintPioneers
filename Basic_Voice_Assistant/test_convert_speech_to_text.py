import unittest
from unittest.mock import patch, MagicMock
import speech_recognition as sr
from voice_text import convert_speech_to_text

class TestConvertSpeechToText(unittest.TestCase):

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')
    def test_convert_speech_to_text_success(self, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
        mock_instance.recognize_google.return_value = "hello world"

        result = convert_speech_to_text()
        assert result == "hello world", f"Expected 'hello world', but got {result}"

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')
    def test_convert_speech_to_text_empty_audio(self, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
        mock_instance.recognize_google.side_effect = sr.UnknownValueError()

        result = convert_speech_to_text()
        assert result == "Sorry, I could not understand the audio.", \
            f"Expected 'Sorry, I could not understand the audio.', but got {result}"

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')
    def test_convert_speech_to_text_silence(self, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
        # Simulate silence leading to an UnknownValueError
        mock_instance.recognize_google.side_effect = sr.UnknownValueError()

        result = convert_speech_to_text()
        assert result == "Sorry, I could not understand the audio.", \
            f"Expected 'Sorry, I could not understand the audio.', but got {result}"

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')
    def test_convert_speech_to_text_request_error(self, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
        mock_instance.recognize_google.side_effect = sr.RequestError()

        result = convert_speech_to_text()
        assert result == "Could not request results from Google Speech Recognition service.", \
            f"Expected 'Could not request results from Google Speech Recognition service.', but got {result}"

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')
    def test_convert_speech_to_text_excessive_length(self, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
        # Simulate long audio input leading to an UnknownValueError
        mock_instance.recognize_google.side_effect = sr.UnknownValueError()

        result = convert_speech_to_text()
        assert result == "Sorry, I could not understand the audio.", \
            f"Expected 'Sorry, I could not understand the audio.', but got {result}"

    @patch('voice_text.sr.Recognizer')
    @patch('voice_text.sr.Microphone')
    def test_convert_speech_to_text_different_language(self, mock_microphone, mock_recognizer):
        mock_instance = mock_recognizer.return_value
        mock_audio = MagicMock()
        mock_instance.listen.return_value = mock_audio
        # Simulate recognizing audio in a different language
        mock_instance.recognize_google.side_effect = sr.UnknownValueError()

        result = convert_speech_to_text()
        assert result == "Sorry, I could not understand the audio.", \
            f"Expected 'Sorry, I could not understand the audio.', but got {result}"

if __name__ == '__main__':
    unittest.main()
