import { StatusBar } from "expo-status-bar";
import React, { useState } from "react";
import {
  StyleSheet,
  Text,
  View,
  Image,
  TouchableOpacity,
  Alert,
} from "react-native";
import { Audio } from "expo-av";
import axios from "axios";
import * as Speech from "expo-speech";

const backgroundcolor = "#3b5998";

const AUDIO_RECORDER_MODE = {
  allowsRecordingIOS: true,
  playsInSilentModeIOS: true,
};

const MULTIPLATFORM_RECORDING_OPTIONS = {
  android: {
    extension: ".m4a",
    outputFormat: Audio.RECORDING_OPTION_ANDROID_OUTPUT_FORMAT_MPEG_4,
    audioEncoder: Audio.RECORDING_OPTION_ANDROID_AUDIO_ENCODER_AAC,
    sampleRate: 44100,
    numberOfChannels: 2,
    bitRate: 128000,
  },
  ios: {
    extension: ".wav",
    outputFormat: Audio.RECORDING_OPTION_IOS_OUTPUT_FORMAT_LINEARPCM,
    audioQuality: Audio.RECORDING_OPTION_IOS_AUDIO_QUALITY_HIGH,
    sampleRate: 44100,
    numberOfChannels: 1,
    linearPCMBitDepth: 16,
    linearPCMIsBigEndian: false,
    linearPCMIsFloat: false,
  },
};

export default function App() {
  const [recording, setRecording] = useState(null);
  const [response, setResponse] = useState(null);
  const [emotion, setEmotion] = useState(null);
  const [text, setText] = useState(null);
  const serverUrl = "http://192.168.4.158:5000/process_audio";

  const checkPermissions = async () => {
    try {
      const { granted } = await Audio.requestPermissionsAsync();
      if (!granted) {
        Alert.alert(
          "Permissions Required",
          "Please enable microphone access in settings to use this feature."
        );
        return false;
      }
      return true;
    } catch (error) {
      console.error("Permission check error:", error);
      Alert.alert("Error", "An error occurred while checking permissions.");
      return false;
    }
  };

  const startRecording = async () => {
    const permissionsGranted = await checkPermissions();
    if (!permissionsGranted) return;

    try {
      console.log("Configuring audio mode...");
      await Audio.setAudioModeAsync(AUDIO_RECORDER_MODE);

      console.log("Preparing recording...");
      const newRecording = new Audio.Recording();
      await newRecording.prepareToRecordAsync(MULTIPLATFORM_RECORDING_OPTIONS);
      await newRecording.startAsync();
      setRecording(newRecording);

      console.log("Recording started successfully.");
    } catch (err) {
      console.error("Error starting recording:", err);
      Alert.alert(
        "Recording Error",
        "Session activation failed. Ensure no other apps are using the microphone."
      );
    }
  };

  const stopRecording = async () => {
    try {
      console.log("Stopping recording...");
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      setRecording(null);
      console.log("Recording stopped. URI:", uri);

      if (uri) {
        console.log("Preparing audio for upload...");
        const formData = new FormData();
        formData.append("audio", {
          uri,
          type: "audio/wav",
          name: "recording.wav",
        });

        console.log("FormData prepared:", formData);

        const serverResponse = await axios.post(serverUrl, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        setEmotion(serverResponse.data.emotion);
        setText(serverResponse.data.text);
        setResponse(serverResponse.data.response);
        Speech.speak(serverResponse.data.response, {
          language: "en-US", // Optional: Set the language
          pitch: 1.0, // Optional: Set pitch
          rate: 1.0, // Optional: Set speech rate
        });
      }
    } catch (err) {
      console.log("FormData parts:", formData._parts);
      console.error("Error stopping recording or sending audio:", err);

      Alert.alert("Error", "Could not process the recording.");
    }
  };

  const handleMicPress = async () => {
    if (recording) {
      await stopRecording();
    } else {
      await startRecording();
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Emotion & LLM App</Text>
      <View style={styles.content}>
        <View style={styles.micContainer}>
          <TouchableOpacity style={styles.micButton} onPress={handleMicPress}>
            <Image
              source={require("./assets/mic.png")}
              style={styles.micIcon}
            />
          </TouchableOpacity>
          <Text style={styles.speakText}>
            {recording ? "Recording..." : "Press to Speak"}
          </Text>
        </View>
        {emotion && (
          <Text style={styles.resultText}>Detected Emotion: {emotion}</Text>
        )}
        {text && <Text style={styles.resultText}>Recognized Text: {text}</Text>}
        {response && (
          <Text style={styles.resultText}>LLM Response: {response}</Text>
        )}
        <StatusBar style="auto" />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: backgroundcolor,
    alignItems: "center",
    justifyContent: "flex-start",
  },
  title: {
    fontSize: 30,
    fontWeight: "bold",
    color: "#d0d0d0",
    marginTop: 60,
    textAlign: "center",
  },
  content: {
    flex: 1,
    justifyContent: "flex-start",
    alignItems: "center",
    marginTop: 150,
  },
  micContainer: {
    marginTop: 50,
    alignItems: "center",
  },
  micButton: {
    width: 100,
    height: 100,
    backgroundColor: "#FFFFFF",
    borderRadius: 50,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 10,
  },
  micIcon: {
    width: 50,
    height: 50,
  },
  speakText: {
    color: "#d0d0d0",
    fontSize: 16,
  },
  resultText: {
    color: "#ffffff",
    fontSize: 14,
    marginTop: 20,
    paddingHorizontal: 10,
    textAlign: "center",
  },
});
