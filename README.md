# Converso AI Python Library

Converso AI - Python Library  is a Python client for interacting with the Converso AI API.

---

## 🚀 Features
- Fetch available models
- Retrieve API tokens (requires API key)
- Generate images from text prompts (requires API key)
- Fetch previously generated images (requires API key)

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

### For Get Models
```python
# Get Converso AI All Models
models = client.get_models()
print(models)
```
### For Get tokens
```python
# Get Remaining Tokens
tokens = client.get_tokens()
print(tokens)
```

### For Generate image
```python
# Generate Image
image_response = client.generate_image(prompt="A futuristic cityscape", model="model-id")
print(image_response)
```

### For Get all generated images
```python
# Get All Generated Images
images = client.get_generated_images()
print(images)
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
