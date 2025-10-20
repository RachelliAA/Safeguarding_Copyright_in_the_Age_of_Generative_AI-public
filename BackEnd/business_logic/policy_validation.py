# Pydantic Model for Policy Validation
from typing import Dict, List, Optional
from pydantic import BaseModel, ValidationError


class EnforcementMethod(BaseModel):
    name: str
    threshold: float

class PolicySchema(BaseModel):
    name: str
    domain: str
    description: str
    scope: str
    constraints: List[str]
    prohibited_actions: List[str]
    parameters: Dict[str, Optional[str]]
    enforcement: Dict[str, List[EnforcementMethod]]
    created_at: str
    updated_at: str
    status: str
    version: int

def validate_policy(data) -> Optional[PolicySchema]:
    try:
        return PolicySchema(**data)
    except ValidationError as e:
        print("Validation error")
        print(e.json())
        return None
