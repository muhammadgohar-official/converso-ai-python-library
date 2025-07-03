import requests

class ConversoAI:
    BASE_URL = "https://api.stylefort.store"

    def __init__(self, api_key=None):
        """
        Initialize the client with an optional API key.
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

    def get_models(self):
        """
        Fetch available models.
        """
        url = f"{self.BASE_URL}/models"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_tokens(self):
        """
        Fetch tokens (requires API key).
        """
        url = f"{self.BASE_URL}/tokens"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def generate_image(self, prompt, model):
        """
        Generate image from a prompt and model.
        """
        url = f"{self.BASE_URL}/v1/images/generations"
        payload = {"prompt": prompt, "model": model}
        headers = self._get_headers()
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_generated_images(self):
        """
        Fetch previously generated images (requires API key).
        """
        url = f"{self.BASE_URL}/v1/images/generated"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
