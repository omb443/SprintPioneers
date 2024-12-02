import SwiftUI
import AVFoundation

struct ContentView: View {
    @State private var inputText: String = ""
    @State private var responseText: String = "Awaiting response..."
    @State private var isProcessing: Bool = false
    @State private var isRecording: Bool = false

    private let synthesizer = AVSpeechSynthesizer()

    init() {
        configureAudioSession()
    }

    var body: some View {
        VStack(spacing: 20) {
            Text("AI Voice Assistant")
                .font(.largeTitle)
                .fontWeight(.bold)

            TextField("Enter your message here", text: $inputText)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            HStack {
                Button(action: {
                    isRecording = true
                    startSpeechRecognition { recognizedText in
                        DispatchQueue.main.async {
                            if let text = recognizedText {
                                inputText = text
                            } else {
                                responseText = "Could not recognize speech."
                            }
                            isRecording = false
                        }
                    }
                }) {
                    Text(isRecording ? "🎙️ Listening..." : "🎤 Speak")
                        .padding()
                        .background(isRecording ? Color.red : Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                
                Button(action: {
                    isProcessing = true
                    sendTextToBackend(input: inputText) { response in
                        DispatchQueue.main.async {
                            responseText = response ?? "Error communicating with the server."
                            if let response = response {
                                speakText(response)
                            }
                            isProcessing = false
                        }
                    }
                }) {
                    Text(isProcessing ? "Processing..." : "Send")
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .disabled(isProcessing || inputText.isEmpty)
            }

            if isProcessing {
                ProgressView("Processing...")
                    .padding()
            }

            Text(responseText)
                .padding()
                .multilineTextAlignment(.center)
                .font(.headline)
                .foregroundColor(.gray)
        }
        .padding()
        .onTapGesture {
            UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
        }
    }

    func speakText(_ text: String) {
        let utterance = AVSpeechUtterance(string: text)
        utterance.voice = AVSpeechSynthesisVoice(language: "en-US")
        utterance.rate = AVSpeechUtteranceDefaultSpeechRate
        utterance.pitchMultiplier = 1.0
        utterance.volume = 1.0

        synthesizer.speak(utterance)
    }

    func configureAudioSession() {
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(.playAndRecord, mode: .default, options: [.defaultToSpeaker])
            try audioSession.setActive(true)
        } catch {
            print("Failed to set audio session category: \(error.localizedDescription)")
        }
    }
}
