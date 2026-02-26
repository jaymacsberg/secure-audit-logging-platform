## Project Purpose

“Secure cloud-native audit logging platform ( API service + structured logging).”

## Deliverable

API runs locally

Endpoints exist: /health, /submit, /status

Structured JSON logs per request

Request IDs included

Reproducible environment via .venv + requirements.txt

## API Contract (v0.1)

Define:

GET /health

##Purpose: Used by monitoring systems and later Kubernetes probes

 Response fields:

  status (e.g., “ok”)

  service (e.g., “api-service”)

  version (e.g., “0.1.0”)

POST /submit

##Purpose: Simulates events that generate audit logs (later forwarded to logging service)

Request fields:

event_type (string)

message (string)

metadata (object/dict, optional)

Response fields:

request_id (uuid)

accepted (boolean)

GET /status

##Purpose: Operator visibility (basic service stats)

Response fields:

uptime_seconds

request_count
Step 4 — Define Structured Logging Schema (v0.1)

Required fields for every request log

 timestamp (ISO-8601)

 level (INFO/WARN/ERROR)

 service (“api-service”)

 request_id (UUID per request)

 method

 path

 status_code

 duration_ms

Recommended (if easy)

 client_ip

 user_agent

Endpoint-specific fields

 For /submit logs:

  event_type

##Why we lock this now

Because when logs become “provenance records”, changing schema later breaks:

 dashboards

 queries

 alerts

 audit validation

In regulated environments, schema stability matters.

##“Run Instructions”

Run locally

 activate venv

 install requirements

 run uvicorn

 test endpoints
