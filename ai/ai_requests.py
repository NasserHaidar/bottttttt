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
    
    def imitation_generate_image(self, prompt, model):
        for i in range(1000000):
            if i % 100000 == 0:
                ic("imitate generating...")
            i**200
        
        with open("assets\\empty_image.png", "rb") as file:
            return file.read()

    def generate_image(self, prompt: str, model: str):
        response = self.client.images.generate(
            prompt = prompt,
            size = "1024x1024",
            model = model
        )
        #get image url
        image_url = response.data[0].url

        #send get request
        image_response = requests.get(image_url)

        #check status code
        if image_response.status_code == 200:
            #return image as bytes object
            return image_response.content
        else:
            #if error
            ic(f"Error: Unable to download image, status code: {image_response.status_code}")
            return None