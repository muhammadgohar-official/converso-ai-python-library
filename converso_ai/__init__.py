import requests

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

    def _handle_response(self, response):
        """
        Improved response handler for API requests.
        """
        if response.status_code == 500:
            print("API Error: Internal server error or temporary overload. Please try again.")
            return None
        if response.status_code == 488:
            print("API Error: Invalid Api key.")
            return None
        if response.status_code >= 400:
            try:
                error_data = response.json()
                print(f"API Error: {error_data.get('error', 'Unknown error')}")
            except requests.exceptions.JSONDecodeError:
                print(f"API Error: Received status code {response.status_code} but could not decode error message.")
            return None
        return response.json()

    def get_models(self):
        """
        Fetch available models.
        """
        url = f"{self.BASE_URL}/models"
        response = requests.get(url)
        return self._handle_response(response)

    def get_tokens(self):
        """
        Fetch tokens (requires API key).
        """
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            print("Error: API key is required to fetch tokens.")
            return None
        url = f"{self.BASE_URL}/tokens"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        return self._handle_response(response)

    def generate_image(self, prompt, model='mg1-free'):
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
        return self._handle_response(response)

    def get_generated_images(self):
        """
        Fetch previously generated images (requires API key).
        """
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            print("Error: API key is required to fetch generated images.")
            return None
        url = f"{self.BASE_URL}/v1/images/generated"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        return self._handle_response(response)
