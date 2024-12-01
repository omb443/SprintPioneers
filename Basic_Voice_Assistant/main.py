from flask import Flask, request, jsonify
import basic_llm

app = Flask(__name__)

@app.route('/process-text', methods=['POST'])
def process_text():
    try:
        # Parse JSON input
        data = request.json
        if not data or 'input_text' not in data:
            return jsonify({"error": "Invalid input. 'input_text' key is required."}), 400

        # Process input using the LLM
        input_text = data['input_text']
        response_text = basic_llm.get_response(input_text)

        # Return response
        return jsonify({"response_text": response_text}), 200
    except AttributeError as e:
        return jsonify({"error": f"AttributeError: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
