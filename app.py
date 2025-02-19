from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Add this import
import os
from chatbot import respond

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

app.config['API_KEY'] = os.getenv('API_KEY')

@app.route('/')
def home():
    with app.app_context():
        return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = respond(user_input)
    return jsonify({"response": response})

@app.errorhandler(500)
def internal_error(error):
    return "An internal error occurred.", 500

# Initialize Hugging Face Inference Client
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")

def chatbot(input_text):
    # Check if the input matches any recipe key
    for key in recipes:
        if key.lower() in input_text.lower():
            return recipes[key]
    return "I can help you with recipes! Just ask for a specific dish."

def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    recipe_response = chatbot(message)
    if recipe_response != "I can help you with recipes! Just ask for a specific dish.":
        yield recipe_response
        return

    messages = [{"role": "system", "content": system_message}]

    for user_msg, assistant_msg in history:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({"role": "user", "content": message})

    response = ""
    try:
        for message in client.chat_completion(
            messages,
            max_tokens=max_tokens,
            stream=True,
            temperature=temperature,
            top_p=top_p,
        ):
            token = message.choices[0].delta.content
            response += token
            yield response
    except Exception as e:
        yield f"An error occurred: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)