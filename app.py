from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from huggingface_hub import InferenceClient  # Ensure this is correctly imported

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Hugging Face Inference Client
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"response": "Please send a valid message."}), 400

        user_input = data['message']
        print(f"User Input: {user_input}")  # Debugging log

        response = get_ai_response(user_input)
        print(f"AI Response: {response}")  # Debugging log

        return jsonify({"response": response})
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Print error to logs
        return jsonify({"response": f"Internal error: {str(e)}"}), 500  # Return error details

@app.errorhandler(500)
def internal_error(error):
    print("Internal Server Error:", error)  # Log the error
    return jsonify({"response": "An internal error occurred."}), 500

def get_ai_response(message):
    """
    Uses the Hugging Face model to generate a chatbot response.
    """
    try:
        print("Sending request to Hugging Face API...")  # Debugging log
        response = client.text_generation(message, max_new_tokens=100)  # Correct API call
        print("Response received from Hugging Face API:", response)  # Debugging log
        return response
    except Exception as e:
        print(f"Error calling Hugging Face API: {str(e)}")  # Log error
        return "I'm having trouble responding right now."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Dynamically set port
    print(f"Starting Flask app on port {port}...")  # Debugging log
    app.run(host='0.0.0.0', port=port, debug=True)