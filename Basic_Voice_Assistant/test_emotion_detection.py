import unittest
import numpy as np
from unittest.mock import patch, MagicMock
from emotion_detection import noise, stretch, shift, pitch, extract_features, get_features, predict

class TestEmotionDetection(unittest.TestCase):

    def setUp(self):
        
        self.sample_data = np.random.rand(1000)  
        self.sample_rate = 22050  
    def test_noise(self):
        noisy_data = noise(self.sample_data)
        
        self.assertEqual(noisy_data.shape, self.sample_data.shape)
        
        self.assertFalse(np.array_equal(noisy_data, self.sample_data))

    def test_stretch(self):
        stretched_data = stretch(self.sample_data)
       
        self.assertIsInstance(stretched_data, np.ndarray)

    def test_shift(self):
        shifted_data = shift(self.sample_data)
        
        self.assertEqual(shifted_data.shape, self.sample_data.shape)

    def test_pitch(self):
        pitched_data = pitch(self.sample_data, self.sample_rate)
        
        self.assertEqual(pitched_data.shape, self.sample_data.shape)

    def test_extract_features(self):
        features = extract_features(self.sample_data)
       
        self.assertIsInstance(features, np.ndarray)
        
        self.assertGreater(features.size, 0)

    def test_get_features(self):
        features = get_features(self.sample_data)
       
        self.assertEqual(features.shape[0], 3)  
       
        self.assertGreater(features.size, 0)

    @patch('emotion_detection.load_model')
    def test_predict(self, mock_load_model):
      
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([[0.1, 0.1, 0.1, 0.1, 0.1, 0.5]])  

      
        mock_audio = MagicMock()
        mock_audio.get_raw_data.return_value = (np.random.rand(162) * 32767).astype(np.int16).tobytes()

       
        emotion = predict(mock_audio)

      
        self.assertIsInstance(emotion, str)
      
        self.assertIn(emotion, ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad'])

if __name__ == '__main__':
    unittest.main()
