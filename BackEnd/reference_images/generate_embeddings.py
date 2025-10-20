from PIL import Image
import torch
import clip
import os
from pymongo import MongoClient
from core.config import settings

# Load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Connect to MongoDB Atlas
client = MongoClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]
collection = db["reference_images"]

# Folder with your images
image_folder = "reference_images/images"

for filename in os.listdir(image_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        image_path = os.path.join(image_folder, filename)
        image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

        with torch.no_grad():
            embedding = model.encode_image(image).squeeze().tolist()

        doc = {
            "filename": filename,
            "embedding": embedding
        }# add iconic features 

        collection.insert_one(doc)
        print(f"Inserted: {filename}")


# run like this: python -m reference_images.generate_embeddings
