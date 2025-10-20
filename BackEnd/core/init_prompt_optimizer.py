# app/services/prompt_optimizer.py

import dspy
#from core.config import settings
# Internal state
_initialized = False
_refiner = None

def init_prompt_optimizer():
    """Initialize the prompt optimization engine (e.g., DSPy)."""
    global _initialized, _refiner

    if _initialized: # if it already exists, no need to reinitialize
        return

    lm = dspy.LM(model="gpt-4o-mini", temperature=0.3) # lm is a language model used for prompt optimization
    dspy.settings.configure(lm=lm)

    _refiner = dspy.Predict(
        "desired_prompt: str, current_image: dspy.Image, current_prompt: str, tweak_instructions:str -> feedback: str, safe_and_sufficiently_similar: bool, image_strictly_matches_desired_prompt: bool, revised_prompt: str"
    )

    _initialized = True
    print("[PromptOptimizer] Initialized.")

# Get the prompt refiner instance
def get_prompt_optimizer():
    """Call the DSPy optimizer with current prompt context."""

    if _refiner is None:
        raise RuntimeError("Prompt optimizer not initialized. Call init_prompt_optimizer() first.")
    return _refiner
