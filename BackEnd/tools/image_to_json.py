import base64
import json
from together import Together
# import tkinter as tk
# from tkinter import filedialog
from core.config import settings
from .tool_validation import ImageDescription
import re

def _extract_json(content):
    """
    Remove markdown code fences and language tags from model output.
    """
    # Remove code fences and language tags
    content = re.sub(r"^```[a-zA-Z]*\s*", "", content)
    content = re.sub(r"\s*```$", "", content)
    return content.strip()

class ImageToJsonTool:
    def __init__(self, api_key=settings.TOGETHERAI_API_KEY, model_name: str= settings.TOGETHERAI_MODEL):
        
        self.api_key = api_key
        self.model_name = model_name
        self.client = Together(api_key=api_key)

    def encode_image_to_data_url(self, image_path):
        with open(image_path, "rb") as img_file:
            b64_image = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{b64_image}"

    def analyze_caricature(self, image_path: str) -> ImageDescription | None:
        if not image_path:
            raise ValueError("No image path provided.")

        image_data_url = self.encode_image_to_data_url(image_path)

        system_prompt = (
            "You are a visual intelligence assistant. "
            "Your job is to analyze caricature-style images and return structured JSON describing characters, scenes, buildings, vehicles, and celebrities. "
            "Please be concise and avoid repeating elements or adding unnecessary information like quotes or celebrity names unless explicitly asked."
        )

        user_prompt = """
Return ONLY a valid JSON object with the following structure:

{
  "asset_type": "Image",
  "character": {
    "hairstyle": "Hair description",
    "outfit": "Clothing details",
    "accessories": "Any visible accessories",
    "color_scheme": "Dominant color palette",
    "facial_features": "Unique or exaggerated features",
    "expression": "Facial expression",
    "pose": "Body pose or gesture",
    "body_proportions": "Exaggerated or stylized body parts"
  },
  "scene": {
    "location": "Indoor or outdoor setting",
    "lighting": "Type of lighting (e.g. studio, natural)",
    "objects_present": "Visible objects",
    "weather": "Weather conditions, if applicable"
  },
  "building": {
    "architecture_style": "Type of architecture",
    "windows": "Window features",
    "doors": "Door type",
    "landmark_name": "Recognizable building name"
  },
  "vehicle": {
    "vehicle_type": "Type (car, truck, etc.)",
    "brand_logos": "Visible brand logos",
    "color": "Vehicle color",
    "license_plate": "Text of plate, if readable"
  },
  "celebrity": {
    "name": "Celebrity name if identifiable",
    "facial_similarity_score": "Float from 0 to 1",
    "age_estimation": "Estimated age",
    "quotes": "Famous quote or known line"
  }
}
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt.strip()},
                        {"type": "image_url", "image_url": {"url": image_data_url}},
                    ],
                },
            ],
        )

        try:
            cleaned_content = _extract_json(response.choices[0].message.content)
            raw_output = json.loads(cleaned_content)
            # Validate and parse with Pydantic model
            return ImageDescription.parse_obj(raw_output)
        except json.JSONDecodeError:
            print("Could not parse model response as JSON:")
            print(response.choices[0].message.content)
            return None
        except Exception as e:
            print(f"Validation error: {e}")
            return None

# Schema attachment (for FastAPI or doc generation)
ImageToJsonTool.analyze_caricature.schema = json.dumps({
    "type": "object",
    "properties": {
        "image_path": {
            "type": "string",
            "description": "Path to the caricature-style image to be analyzed."
        }
    },
    "required": ["image_path"]
})

