# Converso AI Python Library

Converso AI - Python Library is a Python client for interacting with the Converso AI API.

---

## 🚀 Features
- Fetch available models
- Retrieve API tokens (requires API key)
- Generate images from text prompts (requires API key)
- Fetch previously generated images (requires API key)
- Generate chat completions (requires API key)

---

## 📦 Installation

```bash
pip install converso-ai
```

---

## 💻 Example Usage

```python
from converso_ai import ConversoAI

# Initialize client
client = ConversoAI(api_key="YOUR_API_KEY")
```

### Get Available Models
```python
models = client.models()
print(models)
```

### Get Tokens
```python
tokens = client.tokens()
print(tokens)
```

### Generate Image
```python
# Generate Image
image_response = client.generate_image(prompt="A futuristic cityscape", model="model-id")
print(image_response)
```

### Get All Generated Images
```python
# Get All Generated Images
images = client.generated_images()
print(images)
```

### Generate Chat Completion
```python
# Generate a completion
messages = [
    {"role": "user", "content": "Hello, who are you?"},
    # ... more messages ...
]
completion_response = client.chat_completion(model="MODEL_ID", messages=messages)
print(completion_response)
```

---

## ⚙ Project Structure

```
converso_ai/
├── converso_ai/
│   └── __init__.py        # Library code
├── pyproject.toml         # Package config
├── requirements.txt       # Dependencies
├── README.md              # This file
└── LICENSE                # License file (optional)
```

---

## 📖 API Docs

Official API documentation: [https://conversoai.stylefort.store](https://conversoai.stylefort.store)

---

## 📝 License

MIT License. See `LICENSE` file for details.
