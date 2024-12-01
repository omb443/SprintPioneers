//
//  APIService.swift
//  VoiceAssistant
//
//  Created by om boghra on 01/12/24.
//

import Foundation

func sendTextToBackend(input: String, completion: @escaping (String?) -> Void) {
    guard let url = URL(string: "http://127.0.0.1:5001/process-text") else {
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
            completion(nil)
            return
        }

        guard let data = data else {
            completion(nil)
            return
        }

        let jsonResponse = try? JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
        completion(jsonResponse?["response_text"] as? String)
    }.resume()
}
