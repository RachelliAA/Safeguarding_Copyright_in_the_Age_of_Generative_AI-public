import base64
import uuid
import os
from core.init_vision_model import get_vision_model_client
from database.action_DB import ActionDB
from business_logic.action import Action
from core.init_prompt_optimizer import get_prompt_optimizer
#import requests  # external library

from PIL import Image as PILImage
from io import BytesIO
#import random


class ImageGen:
    def __init__(self, model: str, storage: str, provider: str = "together.ai"):
        """
        Image generation service.

        Args:
            model (str): The model name to use for image generation.
            storage (ImageStorage): An instance of the storage backend.
            provider (str): Image generation provider (default: "together.ai").
        """
        self.provider = provider
        self.model = model
        self.storage = storage
        self.client = get_vision_model_client()

        # Image generation attributes
        self.prompt = None  # the prompt that generated the image.
        self.image_id = None  # id of the image
        self.image_data = None  # the raw image bytes
        self.image_url = None  # link to s3
        self.image_name_storage = None  # the name of the file in s3
        self.image_base64 = None  # the image in base64
        self.local_image_path = None  # path to the local image file

    def sanitize_filename(self, text: str) -> str:
        import re
        # Replace any character that is NOT a-z, A-Z, 0-9, underscore, or dash with underscore
        sanitized = re.sub(r'[^A-Za-z0-9_\-]', '_', text)
        return sanitized

    async def generate_image(self, prompt: str, save_to_storage: bool = False) -> dict:
        """Main image generation pipeline."""
        self.prompt = prompt
        print(f"\n\nGenerating image with prompt: {prompt}")

        if self.provider != "together.ai":
            raise NotImplementedError(f"Provider '{self.provider}' not implemented.")

        while True:
            try:
                response = self.client.images.generate(
                    prompt=prompt,
                    model=self.model,
                    width=1024,
                    height=768,
                    steps=4,
                    n=1,
                    response_format="b64_json"
                )
                break  # Break the loop if generation is successful

            except Exception as e:
                if "422" in str(e):
                    print("NSFW filter triggered. Retrying with same prompt...")
                    continue  # Retry the same prompt
                else:
                    raise  # Reraise any other unexpected exceptions

        self.image_base64 = response.data[0].b64_json
        self.image_data = base64.b64decode(response.data[0].b64_json)

        # Ensure directory exists
        os.makedirs("static/generated", exist_ok=True)

        # Sanitize prompt for filename
        safe_prompt = self.sanitize_filename(prompt[:30])
        file_path = f"static/generated/{safe_prompt}.png"
        self.local_image_path = file_path
        with open(file_path, "wb") as f:
            f.write(self.image_data)

        self.image_name_storage = str(uuid.uuid4())

        if save_to_storage:
            print("saving image to storage")
            self.image_url = self.insert_image()
            print("Image saved to storage with URL:", self.image_url)
            self.image_id = self.insert_user_action()
            print("Image generation action inserted with ID:", self.image_id)
        else:
            print("NOT saving image to storage")

        return self

    def insert_image(self) -> str:
        """
        Saves the image to storage.

        Returns:
            str: URL or key of the saved image.
        """
        return self.storage.save_image(self)

    def insert_user_action(self) -> str:
        """
        Saves the image generation action to the database.

        Returns:
            str: Database record ID.
        """
        action_db = ActionDB()
        action = Action(
            action_db=action_db,
            model=self.model,
            provider=self.provider,
            user_id=1,  # TODO: Replace with dynamic user ID if needed
            prompt=self.prompt,
            image_url=self.image_url,
        )
        print("Action in imagegen", action)
        image_id = action.insert_action()
        print("Image generation action inserted with ID:", image_id)
        return image_id

    def get_image(self, image_id: str):
        return self.storage.get_image(image_id)

    def delete_image(self, image_id: str):
        return self.storage.delete_image(image_id)



    async def prompt_iteration(self, prompt: str, input_image_base64: str, reason_of_breach: str, max_iter: int = 5) -> dict:
        
        """Perform iterative DSPy prompt refinement starting with the given image and appended breach reason."""
        
        print("Starting prompt iteration...")
        
        optimizer = get_prompt_optimizer()

        current_prompt = f"{prompt}\n\n"
        print(f"reason of breach: {reason_of_breach}")
        core_concept = prompt

        tweak_instructions = f"""
           PLACE HOLDER
           instructions for llm to tweak the prompt for the prompt iteration
            """



        self.image_base64 = input_image_base64
        self.image_data = base64.b64decode(self.image_base64) #turns into raw data
        current_image = PILImage.open(BytesIO(self.image_data))# prepare the image for the optimizer


        for i in range(max_iter):
            print(f"[Iteration {i+1}] Prompt: {current_prompt}")

            if i > 0:
                # Only generate new image from 2nd iteration onwards
                # Call your existing generate_image method
                await self.generate_image(prompt=current_prompt, save_to_storage=False)
                self.image_data = base64.b64decode(self.image_base64)
                current_image = PILImage.open(BytesIO(self.image_data)) # prepare for the optimizer
                print("Generated new image.")

            # Save image locally
            os.makedirs("static/iterations", exist_ok=True)#make sure the directory exists
            file_path = f"static/iterations/{self.sanitize_filename(prompt[:30])}_{i+1}.png"
            
            with open(file_path, "wb") as f:
                f.write(self.image_data)
            print(f"Saved image to {file_path}")

            result = optimizer(
                desired_prompt=core_concept,
                current_image=current_image,
                current_prompt=current_prompt,
                tweak_instructions=tweak_instructions
            )
            print("\n\nOptimizer result:", result)
            if result.safe_and_sufficiently_similar:
                #final_image_url = None  # handled externally or irrelevant if base64
                #revised_prompt = result.revised_prompt
                print("image finished after iteration:", i+1)
                break
            
            revised_prompt = result.revised_prompt


            print(f"→ Revised prompt: {revised_prompt}")
            print(f"   Feedback: {result.feedback}")

            if revised_prompt == current_prompt or not revised_prompt:
                print("No further meaningful revisions; stopping.")
                break

         

            current_prompt = revised_prompt
            #core_concept = revised_prompt

        final_image_data = self.image_data
        self.image_base64 = base64.b64encode(final_image_data).decode("utf-8")#the image in base64
        self.prompt = current_prompt

        print("Final prompt:", self.prompt)
        return self
