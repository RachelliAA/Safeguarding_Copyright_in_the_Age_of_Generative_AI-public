import json
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_CONFIG_PATH = Path(__file__).resolve().parent.parent / "settings.base.json"

class Settings(BaseSettings):
    # --- Static Config from JSON ---
    PROJECT_NAME: str
    ENV: str
    OPENAI_MODEL: str
    IMAGE_MODEL_NAME: str 
    TOGETHERAI_MODEL: str
    CLIP_MODEL_NAME: str
    AWS_REGION: str
    USERS_COLLECTION: str
    POLICIES_COLLECTION: str
    ACTIONS_COLLECTION: str
    ASSESSMENTS_COLLECTION: str
    


    # --- Secret / Environment-based config ---
    MONGO_URI: str = Field(..., env="MONGO_URI")
    DATABASE_NAME: str = Field(..., env="DATABASE_NAME")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    TOGETHERAI_API_KEY: str = Field(..., env="TOGETHERAI_API_KEY")
    AWS_ACCESS_KEY_ID: str = Field(..., env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET: str = Field(..., env="AWS_S3_BUCKET")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Load JSON config and override with env
with open(BASE_CONFIG_PATH) as f:
    json_config = json.load(f)
print(json_config)  # Debug output

# Pass to Settings
settings = Settings(**json_config)
