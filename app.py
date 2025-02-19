import gradio as gr
from huggingface_hub import InferenceClient
from recipes import recipes  # Import recipes dictionary
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.config['API_KEY'] = os.getenv('API_KEY')
from chatbot import respond
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
    """Handles basic questions and recipe responses."""
    
    # If the user asks about the creator
    creator_questions = [
        "who created you",
        "who made you",
        "who is your creator",
        "who developed you",
        "who is your creator"
    ]
    
    for question in creator_questions:
        if question in input_text.lower():
            return "I was created by Nicholas Levi Rianto!!"

    # If no recipe or creator question is found, return a generic response
    return "I can help you with recipes! Just ask for a specific dish."
    
    # Check if the input matches any recipe key
    for key in recipes:
        if key.lower() in input_text.lower():
            return recipes[key]

def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    # Check if the message is related to recipes
    recipe_response = chatbot(message)
    if recipe_response != "I can help you with recipes! Just ask for a specific dish.":
        yield recipe_response
        return

    # Prepare messages for the Hugging Face model
    messages = [{"role": "system", "content": system_message}]

    for user_msg, assistant_msg in history:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({"role": "user", "content": message})

    # Stream response from Hugging Face model
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

# Gradio ChatInterface
demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Textbox(value="You are a friendly Chatbot.", label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.95,
            step=0.05,
            label="Top-p (nucleus sampling)",
        ),
    ],
)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)