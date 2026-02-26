import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    """
    Formats log records as one-line JSON.
    This is critical for observability tools (ELK/OpenSearch/Loki) and audit pipelines.
    """

    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # Include "extra" fields if present
        # (FastAPI handlers will supply these)
        for key in [
            "service",
            "request_id",
            "method",
            "path",
            "status_code",
            "duration_ms",
            "client_ip",
            "user_agent",
            "event_type",
        ]:
            if hasattr(record, key):
                payload[key] = getattr(record, key)

        return json.dumps(payload, ensure_ascii=False)


def get_logger(name: str = "api-service") -> logging.Logger:
    """
    Creates a logger configured to emit structured JSON logs to stdout.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if this function is called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    logger.propagate = False
    return logger