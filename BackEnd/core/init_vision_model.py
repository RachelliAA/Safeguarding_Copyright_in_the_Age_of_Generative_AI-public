# app/services/together_client.py

import together
from core.config import settings

together_client = None

def init_vision_model_client():
    print("###############################")
    global together_client
    if together_client is not None:
        print("TogetherAI client already initialized.")
        return  # Already initialized
    together_client = together.Together(api_key=settings.TOGETHERAI_API_KEY)
    print("TogetherAI client initialized.")

def get_vision_model_client():
    if together_client is None:
        raise RuntimeError("TogetherAI client not initialized. Call init_together() first.")
    return together_client
