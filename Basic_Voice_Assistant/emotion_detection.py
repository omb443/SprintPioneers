import pandas as pd
import numpy as np

import os
import sys

import librosa
import librosa.display
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

from IPython.display import Audio

import joblib
from keras.models import load_model

import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

sample_rate = 0.7

def noise(data):
    noise_amp = 0.035*np.random.uniform()*np.amax(data)
    data = data + noise_amp*np.random.normal(size=data.shape[0])
    return data

def stretch(data):
    return librosa.effects.time_stretch(data, rate = 0.8)

def shift(data):
    shift_range = int(np.random.uniform(low=-5, high = 5)*1000)
    return np.roll(data, shift_range)

def pitch(data, sampling_rate, pitch_factor=0.7):
    return librosa.effects.pitch_shift(data, sr=sampling_rate, n_steps=pitch_factor)


def extract_features(data):
    # ZCR
    result = np.array([])
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
    result=np.hstack((result, zcr)) # stacking horizontally

    # Chroma_stft
    stft = np.abs(librosa.stft(data))
    chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    result = np.hstack((result, chroma_stft)) # stacking horizontally

    # MFCC
    mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mfcc)) # stacking horizontally

    # Root Mean Square Value
    rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
    result = np.hstack((result, rms)) # stacking horizontally

    # MelSpectogram
    mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mel)) # stacking horizontally
    
    return result

def get_features(data):
    # duration and offset are used to take care of the no audio in start and the ending of each audio files as seen above.
    #data, sample_rate = librosa.load(path, duration=2.5, offset=0.6)
    
    # without augmentation
    res1 = extract_features(data)
    result = np.array(res1)
    
    # data with noise
    noise_data = noise(data)
    res2 = extract_features(noise_data)
    result = np.vstack((result, res2)) # stacking vertically
    
    # data with stretching and pitching
    new_data = stretch(data)
    data_stretch_pitch = pitch(new_data, sample_rate)
    res3 = extract_features(data_stretch_pitch)
    result = np.vstack((result, res3)) # stacking vertically
    
    return result

def predict(audio):
    #features = get_features(audio)
    #scaler = joblib.load('scaler0.pkl')

    #encoder = joblib.load('onehot_encoder.pkl')

    emotions = ['angry','disgust','fear','happy','neutral','sad']

    #print(features)

    # Convert audio to np.array
    audio_data = audio.get_raw_data()
    audio_np = np.frombuffer(audio_data, dtype=np.int16)

    # Convert to floating-point format and normalize
    audio_np = audio_np.astype(np.float32) / np.max(np.abs(audio_np))

    required_time_steps = 162

    # If audio_np has fewer samples, pad it; if it has more, truncate it
    if audio_np.shape[0] < required_time_steps:
        audio_np = np.pad(audio_np, (0, required_time_steps - audio_np.shape[0]), mode='constant')
    else:
        audio_np = audio_np[:required_time_steps]

    # Reshape to (1, time_steps, 1) to match the model's expected input shape
    audio_np = audio_np.reshape(1, required_time_steps, 1)

    
    # Load the model
    loaded_model = load_model('emotion_model0.h5')

    predicted = loaded_model.predict(audio_np) 

    emotion_index = np.argmax(predicted)

    # Map the index to the corresponding emotion
    emotion = emotions[emotion_index]

    return emotion