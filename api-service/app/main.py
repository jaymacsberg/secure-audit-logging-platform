import os
import time
import httpx
import uuid
from datetime import datetime, timezone

from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from fastapi.responses import PlainTextResponse

from fastapi import BackgroundTasks, FastAPI, Request, Response
from fastapi.responses import JSONResponse

from app.logging_config import get_logger
from app.schemas import HealthResponse, StatusResponse, SubmitRequest, SubmitResponse

SERVICE_NAME = "api-service"
VERSION = "0.1.0"
LOGGING_SERVICE_URL = os.getenv("LOGGING_SERVICE_URL", "http://127.0.0.1:9000")

# Process start time (used for uptime calculation)
START_TIME = time.time()

# Simple in-memory request counter
REQUEST_COUNT = 0

logger = get_logger(SERVICE_NAME)

REQUEST_COUNTER = Counter(
    "api_requests_total",
    "Total number of HTTP requests handled by the API service",
    ["method", "path", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)

async def forward_audit_event(
    request_id: str,
    event_type: str | None,
    metadata: dict | None,
) -> None:
    """
    Sends an audit event to the logging service in the background.

    This keeps the main request path fast and reduces coupling between
    the API response path and the logging pipeline.
    """
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            await client.post(
                f"{LOGGING_SERVICE_URL}/ingest",
                json={
                    "service": SERVICE_NAME,
                    "request_id": request_id,
                    "event_name": "submit_received",
                    "event_type": event_type,
                    "payload": metadata,
                },
            )
    except Exception as exc:
        logger.error(
            "audit_forward_failed",
            extra={
                "service": SERVICE_NAME,
                "request_id": request_id,
                "event_type": event_type,
                "error": str(exc),
            },
        )

app = FastAPI(title=SERVICE_NAME, version=VERSION)

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """
    Runs for every HTTP request:
    - assigns a single request_id
    - measures duration
    - logs request completion in a consistent structured format
    """
    start = time.perf_counter()

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    response = await call_next(request)

    duration_ms = round((time.perf_counter() - start) * 1000, 3)

    duration_seconds = duration_ms / 1000

    logger.info(
        "request_completed",
        extra={
            "service": SERVICE_NAME,
            "request_id": request_id,
            "method": request.method,
            "path": str(request.url.path),
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
        },
    )

    REQUEST_COUNTER.labels(
        method=request.method,
        path=str(request.url.path),
        status_code=str(response.status_code),
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        path=str(request.url.path),
    ).observe(duration_seconds)

    return response


def _uptime_seconds() -> int:
    return int(time.time() - START_TIME)


@app.get("/health", response_model=HealthResponse)
async def health(request: Request):
    """
    Health endpoint used for uptime checks and later Kubernetes probes.
    """
    global REQUEST_COUNT
    REQUEST_COUNT += 1

    resp = HealthResponse(status="ok", service=SERVICE_NAME, version=VERSION)

    return resp


@app.get("/status", response_model=StatusResponse)
async def status(request: Request):
    """
    Simple operator-facing status endpoint.
    """
    global REQUEST_COUNT
    REQUEST_COUNT += 1

   
    resp = StatusResponse(uptime_seconds=_uptime_seconds(), request_count=REQUEST_COUNT)

    return resp


@app.post("/submit", response_model=SubmitResponse)
async def submit(
    payload: SubmitRequest,
    request: Request,
    background_tasks: BackgroundTasks,
):
    """
    Accepts an event and returns a request_id.
    In Week 2, events/logs will be forwarded to the dedicated logging microservice.
    """
    global REQUEST_COUNT
    REQUEST_COUNT += 1

    start = time.perf_counter()
    request_id = request.state.request_id
    status_code = 200

    resp = SubmitResponse(request_id=request_id, accepted=True)

    logger.info(
    "submit_received",
    extra={
        "service": SERVICE_NAME,
        "request_id": request_id,
        "event_type": payload.event_type,
    },
)  
    background_tasks.add_task(
    forward_audit_event,
    request_id,
    payload.event_type,
    payload.metadata,
)
    return resp


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Safety net: logs unexpected errors in a structured way.
    """
    logger.error(
        "unhandled_exception",
        extra={
            "service": SERVICE_NAME,
            "request_id": str(uuid.uuid4()),
            "method": request.method,
            "path": str(request.url.path),
            "status_code": 500,
            "duration_ms": 0,
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
        },
    )
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@app.get("/metrics")
async def metrics():
    return PlainTextResponse(
        content=generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )