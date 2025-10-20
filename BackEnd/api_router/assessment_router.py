from fastapi import APIRouter
from business_logic.assessment import Assessment  
import traceback
from fastapi.responses import JSONResponse
from bson.json_util import dumps
from core.init_llm import init_llm_client  
import json

router = APIRouter()
#hide from server
@router.post("/create_assessment")
def create_assessment(image_url: str, policy_id: str):
    try:
        init_llm_client()
        print("inside create_assessment router")
        assessment_service = Assessment(image_url=image_url, policy_id=policy_id)
        results = assessment_service.create_assessment()
        return {"results": results} 
    except Exception as e:
        error_message = f"Error occurred: {e}\n{traceback.format_exc()}"
        print(error_message)
        return {"error": str(e)}


@router.get("/get_assessment/{assessment_id}")
def get_assessment(assessment_id: str):
    assessment_service = Assessment(image_url="", policy_id="")
    result = assessment_service.get_assessment(assessment_id)
    if result:
        # Convert BSON to JSON-compatible format
        return JSONResponse(content=json.loads(dumps(result)))
    return JSONResponse(content={"error": "Assessment not found."}, status_code=404)


@router.delete("/delete_assessment/{assessment_id}")
def delete_assessment(assessment_id: str):
    try:
        assessment_service = Assessment(image_url="", policy_id="")  # Dummy init
        success = assessment_service.delete_assessment(assessment_id)
        return {"success": success}
    except Exception as e:
        return {"error": str(e)}
