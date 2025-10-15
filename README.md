# Local LLM API

This project provides a minimal, self-contained API for running a Hugging Face language model using Docker. It's designed as a straightforward starter template for serving LLMs locally.

The application uses Flask to create a web server and the `transformers` library to load and interact with the model.

---

## Prerequisites

- **Docker**: You must have Docker installed and running on your machine.

---

## How to Run

1. **Clone the Repository**
   
   Clone this project to your local machine.

   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. **Build the Docker Image**
   
   This command builds the Docker image, installing all necessary dependencies. It will be tagged with the name `my-llm-app`.

   ```bash
   docker build -t my-llm-app .
   ```

3. **Run the Docker Container**
   
   This command starts the container and maps port `5001` on your host machine to port `5000` inside the container.

   ```bash
   docker run -p 5001:5000 my-llm-app
   ```

   The first time you run this, it will download the model weights, which may take a few minutes. You'll see "Model loaded successfully!" in the terminal when it's ready.

---

## Testing the API

Once the container is running, you can send requests to it from a **new terminal window** using `curl`.

### Example Request

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the capital of Ireland?"}' \
  http://127.0.0.1:5001/generate
```

### Example Response

The model will return a JSON object with the generated text.

```json
{
  "generated_text": "Dublin"
}
```

*(Note: Your initial test gave "ireland", which can happen with smaller models. A more typical answer is "Dublin".)*

---

## Model Information

### `google/flan-t5-small`

This project uses the `google/flan-t5-small` model by default. Here are some key details:

* **Architecture**: It's based on the T5 (Text-to-Text Transfer Transformer) architecture. This means it's designed to take text as input and produce text as output, making it versatile for many tasks.
* **Fine-tuning**: The "Flan" part stands for **F**ine-tuned **L**a**n**guage **N**et. It was fine-tuned on a massive collection of instructional prompts, which makes it particularly good at following commands and answering questions directly.
* **Size**: This is the "small" version, with about 80 million parameters. It's lightweight (~300MB), making it perfect for running on a local machine without a powerful GPU. Its main purpose is to demonstrate the end-to-end pipeline effectively.


---

## Using a Different Model

It's very easy to swap out the model.

1. **Find a Model**: Browse for other pre-trained models on the [Hugging Face Hub](https://huggingface.co/models). Look for models compatible with the `AutoModelForCausalLM` or `T5ForConditionalGeneration` tasks.

2. **Edit `app.py`**: Open the `app.py` file and change the `model_name` variable on this line:

   ```python
   # Change this line to the desired model from Hugging Face
   model_name = "google/flan-t5-small"
   ```

   For example, to use a small version of GPT-2, you would change it to:

   ```python
   model_name = "distilgpt2"
   ```

3. **Rebuild the Image**: After changing the code, you must rebuild your Docker image for the changes to take effect.

   ```bash
   docker build -t my-llm-app .
   ```

4. **Run the Container**: Run the container again as before. It will now download and use your newly specified model.
