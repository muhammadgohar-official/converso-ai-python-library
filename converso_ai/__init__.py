from typing import List, Optional, Literal, Any
from pydantic import BaseModel, Field, ConfigDict
import requests

class Message(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    role: str
    content: str
    function_call: Optional[dict[str, Any]] = Field(None, alias="functionCall")

class Choice(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    index: int
    message: Message
    finish_reason: Optional[str] = Field(None, alias="finishReason")
    logprobs: Optional[Any] = None

class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    model_type: Optional[str] = None
    choices: List[Choice] = Field(default_factory=list)
    system_fingerprint: Optional[str] = Field(None, alias="systemFingerprint")
    
class ModelInfo(BaseModel):
    access: Literal["free", "normal", "premium"] = Field(default="free")
    id: str = Field(default="")
    name: str = Field(default="")
    provider: str = Field(default="")
    tokens: int = Field(default=0)
    type: Literal["img", "text"] = Field(default="text")

class TokensRemaining(BaseModel):
    remainingTokens: int = Field(default=0)

class Data(BaseModel):
    url: str = Field(default="")

class ImageGenerationResult(BaseModel):
    creation_time: int = Field(alias="Creation Time", default=0)
    prompt: str = Field(alias="Prompt", default="")
    remaining_tokens: int = Field(alias="Remaining Tokens", default=0)
    type: Literal["img", "text"] = Field(default="img")
    data: List[Data] = Field(default_factory=list)

class AgentResponse(BaseModel):
    agent_id: str = Field(default="")
    choices: List[Choice] = Field(default_factory=list)

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
        Initializes the ConversoAI client.

        Args:
            api_key (str, optional): Your ConversoAI API key. This is required for
                                     authenticated operations like fetching tokens,
                                     generating images, and chat completions.
                                     Defaults to None.
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
        Handles different response types and provides more robust error reporting.
        """
        try:
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()
            if response_type == "chat":
                return ChatCompletionResponse(**data)
            elif response_type == "model_info":
                return [ModelInfo(**item) for item in data]
            elif response_type == "tokens_remaining":
                return TokensRemaining(**data)
            elif response_type == "image_generation_result":
                return ImageGenerationResult(**data)
            elif response_type == "agent_response":
                return AgentResponse(**data)
            return AttrDict(data)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - {response.text}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"An unexpected error occurred during the request: {req_err}")
            return None
        except ValueError as val_err: # Includes JSONDecodeError
            print(f"Error decoding JSON response: {val_err} - Response: {response.text}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None


    def models(self) -> Optional[List[ModelInfo]]:
        """
        Fetches a list of available models from the ConversoAI API.

        Returns:
            Optional[List[ModelInfo]]: A list of ModelInfo objects if successful,
                                       otherwise None.
        """
        url = f"{self.BASE_URL}/v1/models"
        try:
            response = requests.get(url)
            return self._handle_response(response, response_type="model_info")
        except requests.RequestException as e:
            print(f"Error: Failed to fetch models. Details: {str(e)}")
            return None

    def tokens(self) -> Optional[TokensRemaining]:
        """
        Fetches the number of remaining tokens for the authenticated user.

        Requires an API key to be set during client initialization.

        Returns:
            Optional[TokensRemaining]: An object containing the remaining token count
                                       if successful, otherwise None.
        """
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            print("Error: API key is required to fetch tokens.")
            return None
        url = f"{self.BASE_URL}/tokens"
        headers = self._get_headers()
        try:
            response = requests.get(url, headers=headers)
            return self._handle_response(response, response_type="tokens_remaining")
        except requests.RequestException as e:
            print(f"Error: Failed to fetch tokens. Details: {str(e)}")
            return None

    def generate_image(self, prompt: str, model: str = 'flux.1-dev', n: int = 1) -> Optional[ImageGenerationResult]:
        """
        Generates an image based on a text prompt using a specified model.

        Requires an API key to be set during client initialization.

        Args:
            prompt (str): The text description for the image to be generated.
            model (str, optional): The name of the image generation model to use.
                                   Defaults to 'flux.1-dev'.
            n (int, optional): The number of images to generate. Defaults to 1.

        Returns:
            Optional[ImageGenerationResult]: An object containing the image generation
                                             results if successful, otherwise None.
        """
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            print("Error: API key is required to generate images.")
            return None
        url = f"{self.BASE_URL}/v1/images/generations"
        payload = {"prompt": prompt, "model": model, "n": n}
        headers = self._get_headers()
        print(f"Generating image...")
        try:
            response = requests.post(url, json=payload, headers=headers)
            return self._handle_response(response, response_type="image_generation_result")
        except requests.RequestException as e:
            print(f"Error: Failed to generate image. Details: {str(e)}")
            return None

    def chat_completion(self, model: str, messages: List[Message]) -> Optional[ChatCompletionResponse]:
        """
        Generates a chat completion response using the specified model and a list of messages.

        Requires an API key to be set during client initialization.

        Args:
            model (str): The name of the chat completion model to use (e.g., 'gpt-4').
            messages (List[Message]): A list of Message objects representing the
                                      conversation history.

        Returns:
            Optional[ChatCompletionResponse]: An object containing the chat completion
                                              response if successful, otherwise None.
        """
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            print("Error: API key is required to generate completions.")
            return None
        url = f"{self.BASE_URL}/v1/chat/completions"
        payload = {"model": model, "messages": messages}
        headers = self._get_headers()
        try:
            response = requests.post(url, json=payload, headers=headers)
            return self._handle_response(response, response_type="chat")
        except requests.RequestException as e:
            print(f"Error: Failed to get chat completion. Details: {str(e)}")
            return None
    
    def agent_response(self, agent_id: str, prompt: str) -> Optional[AgentResponse]:
        """
        Fetches a response from a specific agent using the provided prompt.

        Requires an API key to be set during client initialization.

        Args:
            agent_id (str): The unique identifier of the agent to query.
            prompt (str): The input prompt to send to the agent.

        Returns:
            Optional[AgentResponse]: An object containing the agent's response
                                     if successful, otherwise None.
        """
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            print("Error: API key is required to fetch agent responses.")
            return None
        
        url = f"{self.BASE_URL}/v1/agents/{agent_id}/responses"
        headers = self._get_headers()
        payload = {"prompt": prompt}
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            return self._handle_response(response, response_type="agent_response")
        except requests.RequestException as e:
            print(f"Error: Failed to get response from agent {agent_id}. Details: {str(e)}")
            return None
