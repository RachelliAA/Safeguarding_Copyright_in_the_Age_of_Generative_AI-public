#import json
from fastapi import APIRouter
from database.image_storage import ImageStorage
from business_logic.image_gen import ImageGen
from fastapi.responses import FileResponse
import os
import core.config as settings
from business_logic.assessment import Assessment
from pydantic import BaseModel
from fastapi import HTTPException
import base64

router = APIRouter()

WITH_ASSESSMENT_BEFORE_ITERATION = True  # Global variable to control assessment behavior
WITH_ASSESSMENT_AFTER_ITERATION = True  # Global variable to control assessment behavior
SAVE_TO_STORAGE = True  # Global variable to control saving to storage

async def call_assement(imageGen, with_assessment=True):
    # policy id is hardcoded for now, should be passed as a parameter
    """Call the assessment process with the generated image.""" 
    assessment = Assessment(
        image_data=imageGen.image_data,
        image_url=imageGen.image_url,
        policy_id="682cd8b161a55636df3b07ce"
    )
    if with_assessment:
        print("with assessment")
        assessment_result = await assessment.create_assessment(imageGen.prompt, imageGen.image_data, imageGen.local_image_path)
        breach = assessment_result.get("breach", False)
        violations = assessment_result.get("violations", [])
        print("breach:", breach)
        print("violations:", violations)


    else:
        print("without assessment")
        assessment_result ={
            "assessment_id": None,
            "breach": True,
            "violations": "The image directly depicts Elsa from the Disney movie 'Frozen', including specific hairstyle (long braided white hair), outfit (ice blue strapless gown with a sweetheart neckline and a sheer cape), and the presence of another character, Olaf. The CLIP similarity score of 0.944688618183136 confirms a high resemblance to copyrighted images.",
            "created_at": None,
            "status": "completed"
        }
        #"violations": " The image depicts SpongeBob SquarePants, a copyrighted character, with high fidelity including his signature outfit and home, the pineapple house. The scene and character details closely match the copyrighted material, violating the Character Copyright Respect Policy",
        #"violations": "The image features a character with a high similarity to SpongeBob SquarePants, a copyrighted fictional character. The character is depicted with his distinctive outfit and appearance, including a yellow square body, white shirt, red tie, and brown pants, matching the description and appearance of SpongeBob. The Clip similarity score of 0.9193952679634094 further confirms the close resemblance to the copyrighted character.",
        #"violations": " The image directly depicts Elsa from the Disney movie 'Frozen', including specific hairstyle (long braided white hair), outfit (ice blue strapless gown with a sweetheart neckline and a sheer cape), and the presence of another character, Olaf. The CLIP similarity score of 0.944688618183136 confirms a high resemblance to copyrighted images.",
        #"violations": "The image depicts Darth Vader, a character from the Star Wars franchise, in his recognizable black Sith Lord armor and cape, holding a red lightsaber. The character's helmet with a breathing mask and overall appearance are iconic elements that are copyrighted. The facial similarity score of 0.9 further confirms the high resemblance to the copyrighted character.",
            
    return {
        "imageBase64": base64.b64encode(imageGen.image_data).decode("utf-8"),
        "assessment": assessment_result
    }
  

#factory function returns an instance of the generating image service
def get_image_service(storage):
    return ImageGen(model=settings.settings.IMAGE_MODEL_NAME, storage=storage)

#factory function returns an instance of the storage service
def get_storage_service():
    return ImageStorage()

# Generate image from prompt and then calls assessment, returns the assessment results
@router.get("/generate-image")
async def generate_image_endpoint(prompt: str):
    """API endpoint to generate an image based on the given prompt."""
    print("Prompt received:", prompt)
    storage = get_storage_service()
    image_service = get_image_service(storage)
    imageGen = await image_service.generate_image(prompt, save_to_storage = SAVE_TO_STORAGE)
    #call assessment
    print("$$$$$$$$$$$$$$$$$$$$$\n\n\n generated image")
    result = await call_assement(imageGen, with_assessment=WITH_ASSESSMENT_BEFORE_ITERATION)

    print("$$$$$$$$$$$$$$$$$$$$$$\n\n\n")
    # print("Image generation result:", result)
    return result
    # return imageGen.image_url




class ImageGenerationRequest(BaseModel):
    imageData: str  # base64 with the prefix
    prompt: str
    breach_reason: str

# Generate image with DSPy prompt iteration and breach reason
@router.post("/generate-image-with-iteration")
async def generate_image_with_iteration(request: ImageGenerationRequest, with_assessment: bool = True):
    try:
        print("Received request:")
        print(f"Prompt: {request.prompt}")
        print(f"Breach Reason: {request.breach_reason}")
        print(f"ImageData Prefix: {request.imageData[:30]}...")

        storage = get_storage_service()
        image_service = get_image_service(storage)

        result_iteration_imageGen = await image_service.prompt_iteration(
            prompt=request.prompt,
            input_image_base64=request.imageData.split(",")[1], #removes the prefix
            reason_of_breach=request.breach_reason,
            max_iter= 5
        )

        result_assessment = await call_assement(result_iteration_imageGen, with_assessment=WITH_ASSESSMENT_AFTER_ITERATION)
        #result_assessment = json.dumps(result_iteration)
        #print("result_assessment:" ,result_assessment)
        #result_iteration = result_assessment

        image_response={
            "imageBase64": result_assessment['imageBase64'],
            "assessment": result_assessment['assessment'],
            "finalPrompt": result_iteration_imageGen.prompt
        }
        
        if with_assessment:
                print("with assessment")
                breach = result_assessment.get("breach", False)
                violations = result_assessment.get("violations", [])
                print("breach:", breach)
                if breach:
                    print("violations:", violations)
                    result_iteration_imageGen = await image_service.prompt_iteration(
                    prompt=request.prompt,
                    input_image_base64=request.imageData.split(",")[1], #removes the prefix
                    reason_of_breach=violations,
                    max_iter= 4   # You can adjust the max_iter as needed
                )
                
        return image_response


    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# Get image by ID
@router.get("/get_image/{image_id}")
def get_image_endpoint(image_id: str):
    """API endpoint to retrieve a stored image by ID."""
    storage = get_storage_service()
    image_path = storage.get_image_path(image_id)
    if image_path and os.path.exists(image_path):
        return FileResponse(image_path, media_type="image/png", filename=os.path.basename(image_path))
    return {"error": "Image not found."}

# Delete image by ID
@router.delete("/delete_image/{image_id}")
def delete_image_endpoint(image_id: str):
    """API endpoint to delete a stored image by ID."""
    storage = get_storage_service()
    success = storage.delete_image(image_id)
    return {"success": success}
