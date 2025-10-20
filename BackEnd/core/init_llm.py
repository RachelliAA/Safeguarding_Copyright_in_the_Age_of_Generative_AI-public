
import openai
from core.config import settings

_llm_client = None

def init_llm_client():
    """
    Initializes the OpenAI LLM client using the API key from settings.
    """
    global _llm_client
    if _llm_client is None:
        _llm_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        print("LLM client initialized.")
    else:
        print("LLM client was already initialized.")

def get_llm_client():
    """
    Returns the initialized OpenAI LLM client.
    Raises an error if the client has not been initialized.
    """
    if _llm_client is None:
        raise RuntimeError("LLM client has not been initialized. Call init_llm_client() first.")
    return _llm_client
