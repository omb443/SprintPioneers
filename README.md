# SprintPioneers

**A friendly voice companion, made just for seniors.** Talk naturally to get help with daily health reminders and routines. The system learns each unique voice and adjusts to individual needs over time. Through simple chats, it understands health, habits, and feelings—then offers the right support at the right time. **No tech hassles, just easy conversations with a helper that keeps seniors healthy and independent.**

## Configuration

To configure the project, follow these steps:

### 1.Clone the Repository
git clone https://github.com/omb443/SprintPioneers.git

cd SprintPioneers

### 2.Install Packages Individually
You can also install each required library manually using:

pip install google-generativeai

pip install SpeechRecognition

pip install pyttsx3

### 3.Run the Application
To start the assistant, execute:

python main.py

### Recommended Python Version
This project is developed and tested with Python 3.8 or higher. Ensure you have the correct version installed.

### File Descriptions 
basic_llm.py: Contains the logic for interacting with the Google generative AI.

main.py: The main entry point for the voice-controlled assistant.

test_convert_speech_to_text.py: Contains unit tests for the speech-to-text conversion functionality.

text_speech.py: Manages text-to-speech functionality using the pyttsx3 library.

voice_text.py: Handles the speech recognition process.

