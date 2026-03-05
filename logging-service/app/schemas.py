from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class IngestRequest(BaseModel):
    service: str = Field(..., min_length=1, description="Name of the service sending the event")
    request_id: str = Field(..., min_length=1, description="Correlection ID for the originating request")
    event_name:str = Field(..., min_length=1, description="Event name e.g., submit_received")
    event_type: Optional[str] = Field(default=None, description="Optional domain category/type")
    payload: Optional[Dict[str, Any]] = Field(default=None, description="Optional event payload (keep small)")


class IngestResponse(BaseModel):
    accepted: bool
    log_id: str

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class LogRecord(BaseModel):
    log_id: str
    timestamp: str
    service: str
    request_id: str
    event_name: str
    event_type: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None