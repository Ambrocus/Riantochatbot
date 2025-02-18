from huggingface_hub import InferenceClient
from recipes import recipes  # Import recipes dictionary

# Initialize Hugging Face Inference Client
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")

def chatbot(input_text):
    # Check if the input matches any recipe key
    for key in recipes:
        if key.lower() in input_text.lower():
            return recipes[key]

    # If no recipe found, return a generic response
    return "I can help you with recipes! Just ask for a specific dish."

def respond(message, history, system_message, max_tokens, temperature, top_p):
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
            messages, max_tokens=max_tokens, stream=True, temperature=temperature, top_p=top_p
        ):
            token = message.choices[0].delta.content
            response += token
            yield response
    except Exception as e:
        yield f"An error occurred: {str(e)}"