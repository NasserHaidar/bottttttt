import requests
import json

from icecream import ic
from openai import OpenAI

class AI_Requests():
    def __init__(self, api_key: str) -> None:
        self.client = OpenAI(
            api_key = api_key,
            base_url = "https://api.proxyapi.ru/openai/v1"
        )
        self.dalle3 = "dall-e-3",
        self.dalle2 = "dall-e-2"
    
    def generate_image(self, prompt: str, model: str):
        response = self.client.images.generate(
            prompt = prompt,
            size = "1024x1024",
            model = model
        )

        return response.data[0].url