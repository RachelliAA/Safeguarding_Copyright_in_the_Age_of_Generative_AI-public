# import asyncio
# import requests
# from business_logic.image_gen import ImageGen

# class DummyStorage:
#     def save_image(self, image_id, image_url):
#         # Download and save the image to disk
#         response = requests.get(image_url)
#         with open(f"{image_id}.png", "wb") as f:
#             f.write(response.content)
#         print(f"Image saved as {image_id}.png")

#     def get_image(self, image_id):
#         pass

#     def delete_image(self, image_id):
#         pass

# async def main():
#     storage = DummyStorage()
#     image_gen = ImageGen(
#         provider="together",
#         model="black-forest-labs/FLUX.1-schnell-Free",
#         storage=storage
#     )

#     result = await image_gen.generate_image("A steampunk flying train above the clouds")
#     print("Generated image URL:", result["url"])

# if __name__ == "__main__":

#     asyncio.run(main())
    
#     #import os
#     #print("TOGETHERAI_API_KEY in env:", os.getenv("TOGETHERAI_API_KEY"))

#    # from core.config import settings
#     #settings = Settings()
#    # print("TOGETHERAI_API_KEY in settings:", settings.TOGETHERAI_API_KEY)
  

# Example Usage:
# from backend.database.Image_storage import ImageGenStorage


# storage = ImageGenStorage()
# image_id = "example_image"
# image_bytes = b"your_image_data_here"  # Replace with actual image bytes
# prompt = "A stunning sunset over the ocean."

# storage.save_image(image_id, image_bytes, prompt)
# caption = storage.get_image_caption(image_id)
# print("Stored caption:", caption)

