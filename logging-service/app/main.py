import uuid
from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, Query

from app.schemas import HealthResponse, IngestRequest, IngestResponse, LogRecord
from app.storage import append_event, read_last

SERVICE_NAME = "logging-service"
VERSION = "0.1.0"

app = FastAPI(title=SERVICE_NAME, version=VERSION)


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", service=SERVICE_NAME, version=VERSION)


@app.post("/ingest", response_model=IngestResponse)
async def ingest(payload: IngestRequest):
    """
    Receives an audit event and writes it to append-only storage.
    The logging service assigns:
    - log_id (unique record ID)
    - timestamp (server-side UTC)
    """
    record = LogRecord(
        log_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        service=payload.service,
        request_id=payload.request_id,
        event_name=payload.event_name,
        event_type=payload.event_type,
        payload=payload.payload,
    )

    append_event(record.model_dump())
    return IngestResponse(accepted=True, log_id=record.log_id)


@app.get("/logs", response_model=List[LogRecord])
async def logs(n: int = Query(default=20, ge=1, le=200)):
    """
    Returns last N log records for operator visibility.
    """
    items = read_last(n)
    # Convert dicts to LogRecord objects (validated)
    return [LogRecord(**item) for item in items]
