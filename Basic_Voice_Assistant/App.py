# import os
# from flask import Flask, request, jsonify
# from werkzeug.utils import secure_filename
# from pydub import AudioSegment
# import librosa

# # Import custom modules
# import voice_text
# import text_speech
# import emotion_detection
# import basic_llm

# # Flask setup
# app = Flask(__name__)

# # Configuration
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Ensure upload directory exists
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/process_audio', methods=['POST'])
# def process_audio():
#     if 'audio' not in request.files:
#         return jsonify({'error': 'No audio file provided'}), 400

#     audio_file = request.files['audio']

#     if audio_file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if allowed_file(audio_file.filename):
#         filename = secure_filename(audio_file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         audio_file.save(filepath)

#         try:
#             print("Loading audio file...")
#             # Load the file as an AudioSegment
#             audio_segment = AudioSegment.from_file(filepath)

#             # Pass the AudioSegment to predict()
#             print("Predicting emotion...")
#             emotion = emotion_detection.predict(audio_segment)
#             print(f"Emotion detected: {emotion}")

#             # Clean up temporary file
#             os.remove(filepath)

#             return jsonify({'emotion': emotion})

#         except Exception as e:
#             print(f"Error during processing: {e}")
#             if os.path.exists(filepath):
#                 os.remove(filepath)
#             return jsonify({'error': str(e)}), 500

#     return jsonify({'error': 'Invalid file type'}), 400

# if __name__ == '__main__':
#     app.run(debug=True, host='192.168.4.158', port=5000)

import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import librosa

from keras.models import load_model


# Import custom modules
import voice_text
import text_speech
import emotion_detection
import basic_llm

# Flask setup
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'm4a'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# model = load_model('emotion_.h5')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']

    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 401

    if allowed_file(audio_file.filename):
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)

        try:
            print("Loading audio file...")

            # Load the file as an AudioSegment
            audio_segment = AudioSegment.from_file(filepath)

            # Convert AudioSegment to raw PCM data
            print("Preparing raw audio data...")
            raw_data = audio_segment.raw_data

            # Pass raw audio data to predict()
            print("Predicting emotion...")
            emotion = emotion_detection.predict(audio_segment)
            print(f"Emotion detected: {emotion}")

            # Convert to WAV format for compatibility with speech_recognition
            wav_filepath = filepath.rsplit('.', 1)[0] + ".wav"
            audio_segment.export(wav_filepath, format="wav")
            print(f"Converted audio saved at: {wav_filepath}")

            # Pass the WAV file to the convert_speech function
            print("Converting speech to text...")
            text = voice_text.convert_speech(wav_filepath)
            print(f"Converted text: {text}")
            
            response = basic_llm.get_response(text)
            
            # text_emotion = model.predict(text)
            
            # Clean up temporary file
            os.remove(filepath)

            return jsonify({
                'text': text,
                'response': response,
                # 'text_emotion': text_emotion.tolist() if hasattr(text_emotion, 'tolist') else text_emotion
                'emotion' : emotion
            })


        except Exception as e:
            print(f"Error during processing: {e}")
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid file type'}), 402


if __name__ == '__main__':
    app.run(debug=True, host='192.168.4.158', port=5000)