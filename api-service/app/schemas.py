from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class SubmitRequest(BaseModel):
    event_type: str = Field(..., min_length=1, description="Type/category of the event")
    message: str = Field(..., min_length=1, description="Human-readable message")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional additional data")


class SubmitResponse(BaseModel):
    request_id: str
    accepted: bool


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class StatusResponse(BaseModel):
    uptime_seconds: int
    request_count: int