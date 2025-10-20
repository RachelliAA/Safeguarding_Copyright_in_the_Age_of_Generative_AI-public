import base64
import json
from together import Together
from core.config import settings

class ImageToTextTool:
    def __init__(
        self,
        api_key: str = settings.TOGETHERAI_API_KEY,
        model_name: str = settings.TOGETHERAI_MODEL
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.client = Together(api_key=api_key)

    def encode_image_to_data_url(self, image_path: str) -> str:
        with open(image_path, "rb") as img_file:
            b64_image = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{b64_image}"

    def describe_image(self, image_path: str) -> str:
        if not image_path:
            raise ValueError("No image path provided.")

        image_data_url = self.encode_image_to_data_url(image_path)

        system_prompt = (
            "You are an image description assistant. Your task is to describe only the visible elements of the image "
            "without any speculation or subjective interpretations. Focus on factual descriptions of the objects, "
            "people, scenery, colors, and shapes present in the image. Avoid adding any emotional, personal, or inferred "
            "statements about the scene, including feelings, expressions, moods, or actions that are not directly observable. "
            "Do not include any assumptions about the image or its content. "
            "Your response should be a clear and concise description of the image's visual content."
        )

        user_prompt = "Describe this image based strictly on its visual content. Do not add any emotions, inferred actions, or speculative interpretations."

        content_payload = [
            {"type": "text", "text": user_prompt},
            {"type": "image_url", "image_url": {"url": image_data_url}},
        ]

       
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content_payload}
            ]
        )

        return response.choices[0].message.content

# Add JSON schema for OpenAPI or tool compatibility
ImageToTextTool.describe_image.schema = json.dumps({
    "type": "object",
    "properties": {
        "image_path": {
            "type": "string",
            "description": "Path to the image to be described."
        },
        "reference_images": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "Optional list of image paths to use for comparison."
        }
    },
    "required": ["image_path"]
})
