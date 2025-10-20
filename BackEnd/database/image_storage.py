
from core.init_storage import get_storage_client
from core.config import settings

class ImageStorage:
    def __init__(self):
        self.s3 = get_storage_client()
        self.bucket = settings.AWS_S3_BUCKET #"loraweights" 

    def save_image(self, image):
        # Upload image with metadata (prompt, model and provider stored as metadata)
        self.s3.put_object(
            Bucket=self.bucket,
            Key=f"images/{image.image_name_storage}.png",
            Body=image.image_data,
            Metadata={"image_id": image.image_name_storage}
        )
        image_url = f"https://{self.bucket}.s3.eu-north-1.amazonaws.com/images/{image.image_name_storage}.png"
        return image_url

    def get_image_prompt(self, image_name_storage: str):
        # Retrieve prompt from metadata
        response = self.s3.head_object(Bucket=self.bucket, Key=f"images/{image_name_storage}.png")
        return response["Metadata"].get("prompt")

