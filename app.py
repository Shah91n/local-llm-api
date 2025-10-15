
from flask import Flask, request, jsonify
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch # PyTorch is needed by the transformers library

# --- 1. Initialize our Flask application ---
app = Flask(__name__)

# --- 2. Load the Model and Tokenizer ---
# It's done once when the app starts to avoid reloading on every request.
# This can take a moment, especially the first time it downloads the model.
model_name = "google/flan-t5-small"
print(f"Loading model: {model_name}...")
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
print("Model loaded successfully!")

# --- 3. Define the API endpoint ---
@app.route('/generate', methods=['POST'])
def generate_text():
    """
    This function is called when we send a POST request to the /generate URL.
    The request body should be a JSON object with a "text" key.
    Example: curl -X POST -H "Content-Type: application/json" -d '{"text": "What is the capital of Ireland?"}' http://127.0.0.1:5000/generate
    """
    # Get the JSON data from the request
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' key in request body"}), 400

    input_text = data['text']
    print(f"Received input text: {input_text}")

    # --- 4. Tokenize the input text ---
    # The tokenizer converts our text string into a format the model understands (tensors).
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    # --- 5. Generate the output ---
    # The model processes the tokenized input and generates new tokens as output.
    outputs = model.generate(input_ids, max_length=500) # You can adjust max_length

    # --- 6. Decode the output ---
    # The tokenizer converts the model's output tokens back into a human-readable string.
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Generated text: {generated_text}")

    # Return the result as a JSON object
    return jsonify({"generated_text": generated_text})

# --- 7. Run the Flask app ---
if __name__ == '__main__':
    # '0.0.0.0' makes the app accessible from outside the Docker container
    app.run(host='0.0.0.0', port=5000)