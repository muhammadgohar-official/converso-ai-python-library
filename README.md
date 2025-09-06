# 🤖 Converso AI Python Library

A lightweight and powerful **Python client** for interacting with the [Converso AI API](https://ai.conversoempire.world/).  
Easily integrate AI models, generate images, retrieve tokens, chat with agents, and more — all with just a few lines of code.  

---

## 🚀 Features
- 🔍 Fetch available AI models *(no API key required)*
- 🔑 Retrieve API tokens *(requires API key)*
- 🖼 Generate images from text prompts *(requires API key)*
- 📂 Access previously generated images *(requires API key)*
- 💬 Generate chat completions *(requires API key)*
- 👤 Get responses from specific agents *(requires API key)*

---

## 📦 Installation

Install directly from [PyPI](https://pypi.org/project/converso-ai/):

```bash
pip install converso-ai
```

---

## ⚡ Quick Start

```python
from converso_ai import ConversoAI

# Initialize client
client = ConversoAI(api_key="YOUR_API_KEY")
```

---

## 💻 Usage Examples

### 🔍 Get Available Models

```python
models = client.models()
print(models)
```

### 🔑 Retrieve Tokens

```python
tokens = client.tokens()
print(tokens)
```

### 🖼 Generate an Image

```python
image = client.generate_image(
    prompt="A futuristic cityscape",
    model="flux.1-dev"
)
print(image)
```

### 💬 Generate Chat Completion

```python
messages = [
    {"role": "user", "content": "Hello, who are you?"}
]
completion = client.chat_completion(
    model="gemini-2.5-flash",
    messages=messages
)
print(completion)
```

### 👤 Get Agent Response

```python
response = client.agent_response(
    agent_id="AGENT_ID",
    prompt="What is the weather today?"
)
print(response)
```

---

## 📂 Project Structure

```
converso-ai/
├── converso_ai/
│   └── __init__.py      # Core library code
├── pyproject.toml       # Build & metadata
├── requirements.txt     # Dependencies
├── README.md            # Documentation
└── LICENSE              # License
```

---

## 📖 Documentation

Full API docs: [Converso AI Docs](https://ai.conversoempire.world/)

---

## 📝 License

This project is licensed under the **MIT License**.
See the [LICENSE](./LICENSE) file for details.

---

## 🔒 Privacy Policy

Read our Privacy Policy here: [Privacy Policy](https://ai.conversoempire.world/privacy-policy)

---

## ⭐ Contributing

Contributions are welcome!

* Fork the repo
* Create a feature branch
* Submit a pull request

Help us make **Converso AI Python Library** even better 🚀

---

## ⚡ Quick Links

* 📦 PyPI: [Converso AI](https://pypi.org/project/converso-ai/)
* 📚 Docs: [API Documentation](https://ai.conversoempire.world/)
* 🛠 Source: [GitHub Repository](https://github.com/muhammadgohar-official/converso-ai-python-library)