from ai import ai_requests

AI_requests = ai_requests.AI_Requests("961472e7-1de4-471f-b744-63e25a7a2a91")

def test_upload(file_path: str):
    with open(file_path, "rb") as image_file:
        image_bytes = image_file.read()
        success, image_id = AI_requests.upload_image(image_bytes)
        print(success, image_id)

#image = AI_requests.get_image("c54422db-dbc1-4582-8778-7dc6dd23ce15")
#if image:
#    with open("retrieved_image.jpg", "wb") as image_file:
#        image_file.write(image)
#    print("Image retrieved and saved successfully.")
#else:
#    print("Failed to retrieve image.")

"""images = AI_requests.generate_image(prompt = "cosmos and starts on background, human on Spacesuit ", image_id = "c54422db-dbc1-4582-8778-7dc6dd23ce15")
for image_bytes in images:
    print(image_bytes)"""
"""if image:
    with open("retrieved_image.jpg", "wb") as image_file:
        image_file.write(image)
    print("Image retrieved and saved successfully.")
else:
    print("Failed to retrieve image.")"""

test_upload("")