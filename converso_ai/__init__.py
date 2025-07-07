from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field
import requests

class Message:
    role: str
    content: str
    function_call: Optional[dict[str, any]]

    def __init__(self, data):
        self.role = data.get("role")
        self.content = data.get("content")
        self.function_call = data.get("function_call")

class Choice:
    index: int
    message: Message
    finish_reason: Optional[str]
    logprobs: Optional[any]  # Add more fields if your API returns them

    def __init__(self, data):
        self.index = data.get("index")
        self.message = Message(data.get("message", {}))
        self.finish_reason = data.get("finish_reason")
        self.logprobs = data.get("logprobs")

class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    def __init__(self, data):
        self.prompt_tokens = data.get("prompt_tokens", 0)
        self.completion_tokens = data.get("completion_tokens", 0)
        self.total_tokens = data.get("total_tokens", 0)

class ChatCompletionResponse:
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    system_fingerprint: Optional[str]

    def __init__(self, data):
        self.id = data.get("id")
        self.object = data.get("object")
        self.created = data.get("created")
        self.model = data.get("model")
        self.choices = [Choice(choice) for choice in data.get("choices", [])]
        self.usage = Usage(data.get("usage", {}))
        self.system_fingerprint = data.get("system_fingerprint")

    def dict(self):
        return {
            "id": self.id,
            "object": self.object,
            "created": self.created,
            "model": self.model,
            "choices": [vars(choice) for choice in self.choices],
            "usage": vars(self.usage),
            "system_fingerprint": self.system_fingerprint,
        }
    
class ModelInfo:
    access: Literal["free", "normal", "premium"]
    id: str
    name: str
    provider: str
    tokens: int
    type: Literal["img", "text"]

    def __init__(self, **data):
        super().__init__(**data)
        self.access = data.get("access", "free")
        self.id = data.get("id", "")
        self.name = data.get("name", "")
        self.provider = data.get("provider", "")
        self.tokens = data.get("tokens", 0)
        self.type = data.get("type", "text")
    
    def dict(self):
        return {
            "access": self.access,
            "id": self.id,
            "name": self.name,
            "provider": self.provider,
            "tokens": self.tokens,
            "type": self.type
        }

class TokensRemaining:
    remainingTokens: int

    def __init__(self, **data):
        super().__init__(**data)
        self.remainingTokens = data.get("remaining Tokens", 0)

    def dict(self):
        return {
            "remainingTokens": self.remainingTokens
        }

class GeneratedImage:
    created_at: datetime
    id: int
    model: str
    prompt: str
    url: str

    def __init__(self, **data):
        super().__init__(**data)
        self.created_at = datetime.fromtimestamp(data.get("created_at", 0))
        self.id = data.get("id", 0)
        self.model = data.get("model", "")
        self.prompt = data.get("prompt", "")
        self.url = data.get("url", "")
    
    def dict(self):
        return {
            "created_at": self.created_at.isoformat(),
            "id": self.id,
            "model": self.model,
            "prompt": self.prompt,
            "url": self.url
        }

class ImageGenerationResult:
    creation_time: int
    prompt: str
    remaining_tokens: int
    type: Literal["img", "text"]
    url: str


    def __init__(self, **data):
        self.creation_time = data.get("Creation Time", 0)
        self.prompt = data.get("Prompt", "")
        self.remaining_tokens = data.get("Remaining Tokens", 0)
        self.type = data.get("type", "img")
        self.url = data.get("url", "")

    def dict(self):
        return {
            "creation_time": self.creation_time,
            "prompt": self.prompt,
            "remaining_tokens": self.remaining_tokens,
            "type": self.type,
            "url": self.url
        }


class AttrDict(dict):
    """
    A dictionary that allows attribute access to its keys, recursively.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            self[key] = self._wrap(value)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"No such attribute: {item}")

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def _wrap(cls, value):
        if isinstance(value, dict):
            return cls(value)
        elif isinstance(value, list):
            return [cls._wrap(v) for v in value]
        return value

class ConversoAI:
    BASE_URL = "https://api.stylefort.store"

    def __init__(self, api_key=None):
        """
        Initialize the client with an optional API key.
        
        The API key is required for operations such as fetching tokens, generating images, and fetching generated images.
        """
        self.api_key = api_key

    def _get_headers(self):
        """
        Internal helper to build headers with API key if provided.
        """
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _handle_response(self, response, response_type=None):
        """
        Improved response handler for API requests.
        """
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return None
        data = response.json()
        if response_type == "chat":
            return ChatCompletionResponse(data)
        elif response_type == "model_info":
            return ModelInfo(**data)
        elif response_type == "tokens_remaining":
            return TokensRemaining(**data)
        elif response_type == "generated_image":
            return GeneratedImage(**data)
        elif response_type == "image_generation_result":
            return ImageGenerationResult(**data)
        return AttrDict(data)

    def models(self):
        """
        Fetch available models.
        """
        url = f"{self.BASE_URL}/v1/models"
        response = requests.get(url)
        return self._handle_response(response, response_type="model_info")

    def tokens(self):
        """
        Fetch tokens (requires API key).
        """
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            print("Error: API key is required to fetch tokens.")
            return None
        url = f"{self.BASE_URL}/tokens"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        return self._handle_response(response, response_type="tokens_remaining")

    def generate_image(self, prompt, model='imagen-3'):
        """
        Generate image from a prompt and model.
        """
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            print("Error: API key is required to generate images.")
            return None
        url = f"{self.BASE_URL}/v1/images/generations"
        payload = {"prompt": prompt, "model": model}
        headers = self._get_headers()
        print(f"Generating image...")
        response = requests.post(url, json=payload, headers=headers)
        return self._handle_response(response, response_type="image_generation_result")

    def generated_images(self):
        """
        Fetch previously generated images (requires API key).
        """
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            print("Error: API key is required to fetch generated images.")
            return None
        url = f"{self.BASE_URL}/v1/images/generated"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        return self._handle_response(response, response_type="generated_image")

    def chat_completion(self, model, messages):
        """
        Generate a completion using the specified model and messages array.
        """
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            print("Error: API key is required to generate completions.")
            return None
        url = f"{self.BASE_URL}/v1/chat/completions"
        payload = {"model": model, "messages": messages}
        headers = self._get_headers()
        response = requests.post(url, json=payload, headers=headers)
        return self._handle_response(response, response_type="chat")