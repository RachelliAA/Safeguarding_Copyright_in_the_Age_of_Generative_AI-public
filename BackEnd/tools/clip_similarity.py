#import base64
import json
from PIL import Image
import torch
import clip
from pymongo import MongoClient
#from pydantic import BaseModel
from core.config import settings

class ClipSimilarityTool:
    def __init__(self, mongo_uri=settings.MONGO_URI, db_name=settings.DATABASE_NAME, index_name="image_vector_index"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        self.client = MongoClient(mongo_uri)
        self.collection = self.client[db_name]["reference_images"]
        self.index_name = index_name

    def encode_image(self, image_path: str) -> list[float]:
        """Preprocess and encode the image to CLIP embedding."""
        image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
        with torch.no_grad():
            return self.model.encode_image(image).squeeze().tolist()

    def search_similar_images(self, image_path: str, limit: int = 15, threshold: float = 0.5) -> list[dict]:
        if not image_path:
            raise ValueError("Image path not provided.")
        
        query_embedding = self.encode_image(image_path)

        pipeline = [
            {
                "$vectorSearch": {
                    "index": self.index_name,
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 100,
                    "limit": limit,
                    "score": {
                        "type": "cosine",
                        "threshold": threshold
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "filename": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]

        return list(self.collection.aggregate(pipeline))


# Schema metadata for documentation tools
ClipSimilarityTool.search_similar_images.schema = json.dumps({
    "type": "object",
    "properties": {
        "image_path": {"type": "string", "description": "Path to the image to compare."},
        "limit": {"type": "integer", "default": 15, "description": "Number of similar images to return."},
        "threshold": {"type": "number", "default": 0.5, "description": "Cosine similarity score threshold."}
    },
    "required": ["image_path"]
})
