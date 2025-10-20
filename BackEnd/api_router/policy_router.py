from fastapi import APIRouter
from business_logic.policy import Policy
import traceback

router = APIRouter()

@router.post("/create_policy")
def create_policy(nl_input: str):
    try:
        print("inside create_policy router")
        policy_service = Policy()  # Initializes with default DB
        policy, policy_id = policy_service.create_policy(nl_input)
        return {"policy": policy, "id": policy_id}
    except Exception as e:
        error_message = f"Error occurred: {e}\n{traceback.format_exc()}"
        print(error_message)  # Print full error details in VS Code
        return {"error": str(e)}


@router.get("/get_policy/{policy_id}")
def get_policy(policy_id: str):
    policy_service = Policy()
    return policy_service.get_policy(policy_id)

@router.delete("/delete_policy/{policy_id}")
def delete_policy(policy_id: str):
    policy_service = Policy()
    return {"success": policy_service.delete_policy(policy_id)}
