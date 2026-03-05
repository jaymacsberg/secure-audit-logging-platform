import json
from pathlib import Path
from typing import Any, Dict, List


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LOG_FILE = DATA_DIR / "audit-log.json1"

# ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)


def append_event(event: Dict[str, Any]) -> None:
    """
    Append one event as a single JSON line 9JSONL).
    This is an append-only log format that is easy to stream and audit.
    """
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def read_last(n: int = 20) -> List[Dict[str, Any]]:
    """
    Return the last N events from the log file.
    For Week 2 we keep it simple (no indexing).
    """
    if not LOG_FILE.exists():
        return[]
    
    with LOG_FILE.open("r", encoding="utf-8") as f:
        lines = f.readlines()

        tail = lines[-n:] if n > 0 else lines
        return [json.loads(line) for line in tail if line.strip()]