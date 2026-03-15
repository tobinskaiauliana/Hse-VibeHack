from pydantic import BaseModel
from typing import Dict, Any

class ErrorResponse(BaseModel):
    error: str
    details: Dict[str, Any] = {}