from pydantic import BaseModel  #, Field, ValidationError
from typing import Any, Dict, Optional
from datetime import datetime

class AssessmentSchema(BaseModel):
    title: str
    description: Optional[str]
    image_url: Optional[Any] = None  # accept raw bytes or binary
    policy_id: str
    results: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    status: str
