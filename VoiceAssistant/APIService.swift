// APIService.swift
import Foundation
import Speech
import AVFoundation


func configureAudioSession() {
    let audioSession = AVAudioSession.sharedInstance()
    do {
        try audioSession.setCategory(.playAndRecord, mode: .default, options: [.defaultToSpeaker])
        
        try audioSession.setActive(true)
    } catch {
        print("Failed to set audio session category: \(error.localizedDescription)")
    }
}


func startSpeechRecognition(completion: @escaping (String?) -> Void) {
    SFSpeechRecognizer.requestAuthorization { authStatus in
        DispatchQueue.main.async {
            guard authStatus == .authorized else {
                completion("Speech recognition permission not granted.")
                return
            }

            let speechRecognizer = SFSpeechRecognizer()
            let recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
            let audioEngine = AVAudioEngine()

            guard let speechRecognizer = speechRecognizer, speechRecognizer.isAvailable else {
                completion(nil)
                return
            }

            let inputNode = audioEngine.inputNode
            let recognitionTask = speechRecognizer.recognitionTask(with: recognitionRequest) { result, error in
                if let error = error {
                    print("Speech recognition error: \(error.localizedDescription)")
                    completion(nil)
                    audioEngine.stop()
                    inputNode.removeTap(onBus: 0)
                    return
                }

                if let result = result {
                    completion(result.bestTranscription.formattedString)
                }
            }

            let recordingFormat = inputNode.outputFormat(forBus: 0)
            inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, _ in
                recognitionRequest.append(buffer)
            }

            audioEngine.prepare()
            do {
                try audioEngine.start()
                print("Listening...")
            } catch {
                print("Audio engine error: \(error.localizedDescription)")
                completion(nil)
            }
        }
    }
}

// Function to send text to backend and retrieve response
func sendTextToBackend(input: String, completion: @escaping (String?) -> Void) {
    guard let url = URL(string: "http://192.168.1.155:5001/process-text") else {
        completion("Invalid URL")
        return
    }

    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")

    let body: [String: String] = ["input_text": input]
    guard let jsonData = try? JSONSerialization.data(withJSONObject: body, options: []) else {
        completion("Invalid input data")
        return
    }

    request.httpBody = jsonData

    URLSession.shared.dataTask(with: request) { data, response, error in
        if let error = error {
            print("Error: \(error.localizedDescription)")
            completion("Network error: \(error.localizedDescription)")
            return
        }

        guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
            completion("Server returned an error.")
            return
        }

        guard let data = data else {
            completion("No data received.")
            return
        }

        if let jsonResponse = try? JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
           let responseText = jsonResponse["response_text"] as? String {
            completion(responseText)
        } else {
            completion("Error parsing response.")
        }
    }.resume()
}

// Function to speak text using AVSpeechSynthesizer
func speakText(_ text: String) {
    let utterance = AVSpeechUtterance(string: text)
    utterance.voice = AVSpeechSynthesisVoice(language: "en-US")
    utterance.rate = AVSpeechUtteranceDefaultSpeechRate
    utterance.pitchMultiplier = 1.0
    utterance.volume = 1.0

    let synthesizer = AVSpeechSynthesizer()
    synthesizer.speak(utterance)
}
