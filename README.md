# SprintPioneers

**A friendly voice companion, made just for seniors.** Talk naturally to get help with daily health reminders and routines. The system learns each unique voice and adjusts to individual needs over time. Through simple chats, it understands health, habits, and feelings—then offers the right support at the right time. **No tech hassles, just easy conversations with a helper that keeps seniors healthy and independent.**

## Configuration

To configure the project, follow these steps:

### 1.Clone the Repository

git clone https://github.com/omb443/SprintPioneers.git

cd SprintPioneers

### 2.Open Basic_Voice_Assistant

Open folder in command line

### 3.Gemini key update

Create gemini key from (https://ai.google.dev/gemini-api/docs/api-key). Using own keys is necessary. Replace it with the key inside SprintPioneers/Basic_Voice_Assistance/basic_llm.py.

### 4.Install Packages

pip install -r requirements.txt

### 5.Run the Application
To start the assistant, execute:

python main.py

### 6.Run the IOS application in Xcode with iphone attached with macbook

Run the code, give the required permission. It takes voice as well as text as input and gives responce in text as well as speech.

### Recommended Python Version
This project is developed and tested with Python 3.8 or higher. Ensure you have the correct version installed.

### File Descriptions 
basic_llm.py: Contains the logic for interacting with the Google generative AI.

main.py: The main entry point for the voice-controlled assistant.

test_convert_speech_to_text.py: Contains unit tests for the speech-to-text conversion functionality.

text_speech.py: Manages text-to-speech functionality using the pyttsx3 library.

voice_text.py: Handles the speech recognition process.

