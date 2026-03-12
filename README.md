Secure Audit Logging Platform

A cloud-native audit logging platform designed to produce traceable, structured, and auditable event records across distributed services.

The project demonstrates how application services can generate audit events and forward them to a dedicated logging microservice that records events in an append-only format.

This architecture reflects patterns used in production systems for:

Observability

Compliance

Security auditing

Provenance tracking

It also serves as a foundation for research into secure logging for federated learning systems under the EU AI Act.

Architecture
Client Request
      │
      ▼
API Service (FastAPI)
  - Handles requests
  - Generates correlation ID
  - Emits structured logs
  - Forwards audit events
      │
      ▼
Logging Service (FastAPI)
  - Receives audit events
  - Assigns server timestamp
  - Generates log_id
  - Stores records in append-only JSONL log
      │
      ▼
Append-Only Audit Log
(logging-service/data/audit-log.jsonl)

This separation ensures that application services cannot directly manipulate audit records.



##Current Features
API Service

Provides operational endpoints and produces structured logs.

Endpoints:

Endpoint	Purpose
/health	Service health check (for monitoring / Kubernetes probes)
/status	Basic service metrics
/submit	Simulated event submission

Key capabilities:
Structured JSON logging
Request correlation via request_id
Middleware-based request logging
Asynchronous forwarding of audit events


##Logging Service

Dedicated service for receiving and storing audit events.

Endpoints:

Endpoint	Purpose
/health	Logging service health check
/ingest	Accepts audit events from other services
/logs	Returns recent stored events

Each stored record contains:
log_id
timestamp
service
request_id
event_name
event_type
payload

Events are stored in JSON Lines format (.jsonl) using append-only writes.


##Structured Logging Schema (v0.1)

Each request processed by the API service emits structured logs with the following fields:

Required fields:

timestamp
level
service
request_id
method
path
status_code
duration_ms

Recommended fields:

client_ip
user_agent

Endpoint-specific fields:

event_type

This schema is fixed early because schema drift breaks dashboards, queries, and audit validation in regulated environments.

Quickstart
1. Clone the repository
git clone https://github.com/jaymacsberg/secure-audit-logging-platform.git
cd secure-audit-logging-platform

2. Start the Logging Service
cd logging-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 9000

3. Start the API Service
cd ../api-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

4. Submit an event
curl -X POST http://127.0.0.1:8000/submit \
  -H "Content-Type: application/json" \
  -d '{
        "event_type":"demo",
        "message":"hello",
        "metadata":{"source":"quickstart"}
      }'

5. Verify event was recorded
curl http://127.0.0.1:9000/logs?n=5
Why This Project Exists

Modern AI and healthcare systems require provable traceability of system actions.

A secure audit pipeline must guarantee:
consistent event structure
centralized event recording
tamper-resistant storage
traceable request lifecycle

This project demonstrates the foundational architecture required to support such systems.

# AWS EC2 Deployment

The platform has been deployed on an AWS EC2 Ubuntu instance using Docker Compose.

Services running on EC2:

- API Service (FastAPI) — exposed on port 8000
- Logging Service — exposed on port 9000
- Prometheus — exposed on port 9090

Deployment characteristics:

- Multi-container deployment with Docker Compose
- Publicly accessible API health endpoint
- Audit event forwarding from API service to logging service
- Prometheus scraping application metrics in the cloud

Example cloud endpoints:

- `http://<EC2_PUBLIC_IP>:8000/health`
- `http://<EC2_PUBLIC_IP>:9000/logs?n=5`
- `http://<EC2_PUBLIC_IP>:9090`

This deployment demonstrates cloud-based service orchestration, remote container operations, and observability on AWS infrastructure.

Roadmap
# Progress So Far

## Week 1
- Built API service with structured logging
- Added request correlation IDs
- Implemented middleware-based request logging

## Week 2
- Built dedicated logging microservice
- Added audit event forwarding from API service to logging service
- Implemented append-only JSONL audit storage

## Week 3
- Containerized both services with Docker
- Added Docker Compose for multi-service orchestration
- Externalized service configuration with environment variables

## Week 4
- Added Prometheus metrics instrumentation
- Exposed `/metrics` endpoint
- Added Prometheus scraping through Docker Compose

## Week 5
- Deployed the full platform on AWS EC2
- Installed Docker and Docker Compose on Ubuntu server
- Ran the platform remotely in the cloud
- Verified public API, logging, and Prometheus access

Author
Joshua Bolade
PhD Researcher — Distributed AI Systems
Focus: Secure logging, provenance, and trustworthy AI infrastructure
