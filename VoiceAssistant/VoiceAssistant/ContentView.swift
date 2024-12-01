import SwiftUI

struct ContentView: View {
    @State private var inputText: String = ""
    @State private var responseText: String = "Awaiting response..."
    @State private var isProcessing: Bool = false

    var body: some View {
        VStack(spacing: 20) {
            Text("AI Voice Assistant")
                .font(.largeTitle)
                .fontWeight(.bold)

            TextField("Enter your message here", text: $inputText)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            Button(action: {
                isProcessing = true
                sendTextToBackend(input: inputText) { response in
                    DispatchQueue.main.async {
                        responseText = response ?? "Error communicating with the server."
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

            Text(responseText)
                .padding()
                .multilineTextAlignment(.center)
        }
        .padding()
    }
}
