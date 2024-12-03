import requests
import json
import time

from icecream import ic
from io import BytesIO
from openai import OpenAI

class AI_Requests():
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.leonardo.ai/v1/images'
        self.upload_images_url = "https://cloud.leonardo.ai/api/rest/v1/init-image"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }

    def upload_image(self, image: bytes):
        try:
            # Инициализация загрузки
            response = requests.post(url=self.upload_images_url, json={"extension": "jpg"}, headers=self.headers)
            response.raise_for_status()  # Raises an error for bad responses
            
            upload_data = response.json().get('uploadInitImage', {})
            fields = json.loads(upload_data.get('fields', '{}'))
            upload_url = upload_data.get('url')
            
            if not upload_url or not fields:
                return False, "Upload URL or fields not received."
            
            # Создаем файловый объект из переданных байтов
            files = {'file': ('image.jpg', BytesIO(image), 'image/jpeg')}
            
            # Загрузка изображения
            response = requests.post(url=upload_url, data=fields, files=files)
            response.raise_for_status()  # Raises an error for bad responses
            
            # Проверка статуса загрузки
            upload_id = upload_data.get('id')
            return True, upload_id if upload_id else "Upload successful but no ID returned."
    
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}"
        except json.JSONDecodeError:
            return False, "Failed to decode JSON response."

    def get_image(self, image_id: str) -> bytes:
        try:
            # Construct the URL for retrieving the image
            response = requests.get(f"{self.upload_images_url}/{image_id}", headers=self.headers)
            response.raise_for_status()  # Raises an error for bad responses

            # Parse the JSON response to get the image URL
            image_data = response.json()  # This will correctly parse the JSON response
            print("Image metadata response:", image_data)  # Debug: print the response

            image_url = image_data["init_images_by_pk"]["url"]  # Attempt to access the URL from the parsed JSON

            if not image_url:
                print("No image URL found in the response.")
                return None
            
            # Retrieve the image from the image URL
            response = requests.get(image_url, headers=self.headers)
            response.raise_for_status()  # Raises an error for bad responses

            return response.content  # Return the raw image bytes

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while retrieving the image: {e}")
            return None
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None


    def generate_image(self, prompt: str, image_id: int):
        if not prompt:  # Проверка на пустоту
            print("Ошибка: 'prompt' не может быть пустым.")
            return None
        
        generate_url = "https://cloud.leonardo.ai/api/rest/v1/generations"

        data = {
            "height": 512,
            "modelId": "1e60896f-3c26-4296-8ecc-53e2afecc132",
            "prompt": prompt,
            "width": 512,
            "num_images": 1
        }

        try:
            response = requests.post(generate_url, json=data, headers=self.headers)
            response.raise_for_status()  # Это вызовет ошибку, если код статуса не 200
            generation_id = response.json()['sdGenerationJob']['generationId']
            
            while True:
                image_url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
                #image_url = f"https://cloud.leonardo.ai/api/rest/v1/generations/8f46007e-ff2d-438e-a9a6-dfcba5367eba"
                response = requests.get(image_url, headers = self.headers)
                #ic(response.json())
                if response.json()["generations_by_pk"]["status"] == "COMPLETE":
                    generated_image_id = response.json()["generations_by_pk"]["generated_images"][0]["id"]
                    break
                else:
                    ic("Генерация еще не завершена...")
                    time.sleep(1)
            ic("Генерация завершена")
            return self.control_network_generation(prompt = prompt, generation_id = generated_image_id, image_id = image_id)
        
        except requests.HTTPError as http_err:
            ic(f'HTTP ошибка: {http_err}. Ответ: {response.text}')
            return None
        except Exception as e:
            ic(f"Произошла неожиданная ошибка: {str(e)}")
            return None

    def control_network_generation(self, prompt: str, generation_id: str, image_id: str):
        generate_url = "https://cloud.leonardo.ai/api/rest/v1/generations"
        ic(generation_id)
        ic(image_id)
        data = {
            "height": 512,
            "modelId": "aa77f04e-3eec-4034-9c07-d0f619684628",
            "prompt": prompt,
            "presetStyle": "CINEMATIC",
            "width": 512,
            "photoReal": True,
            "photoRealVersion": "v2",
            "alchemy": True,
            "controlnets": [
                {
                    "initImageId": generation_id, #'bc81e971-6ef4-4e90-bcdf-2fd2a5c8ea69', 
                    "initImageType": "GENERATED",
                    "preprocessorId": 67,
                    "strengthType": "High",
                    "influence": 0.35
                },
                {
                    "initImageId": image_id, 
                    "initImageType": "UPLOADED",
                    "preprocessorId": 67,
                    "strengthType": "High",
                    "influence": 0.85
                }
            ]
        }
        try:
            images = []
            response = requests.post(generate_url, json=data, headers=self.headers)
            response.raise_for_status()
            generation_id = response.json()['sdGenerationJob']['generationId']
            
            while True:
                image_url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
                response = requests.get(image_url, headers = self.headers)
                #ic(response.json())
                if response.json()["generations_by_pk"]["status"] == "COMPLETE":
                    for generated_image in response.json()["generations_by_pk"]["generated_images"]:
                        image_response = requests.get(generated_image["url"], headers = self.headers) # Возможно здесь не правильно обращаюсь
                        ic(generated_image["url"])
                        images.append(image_response.content)
                    break
                else:
                    ic("Смешивание еще не завершено...")
                    time.sleep(1)
            ic("Смешивание завершено") 
            ic(images)
            return images
        except:
            ic(f"Ошибка при создании смешивания: {response.status_code}, {response.text}")
