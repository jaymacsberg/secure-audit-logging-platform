# Secure Audit Logging Platform

A cloud-native audit logging platform designed to produce traceable, structured, and auditable event records across distributed services.

The project demonstrates how application services can generate audit events and forward them to a dedicated logging microservice that records events in an append-only format.

This architecture reflects patterns used in production systems for:

- Observability
- Compliance
- Security auditing
- Provenance tracking
- Reliable service design

It also serves as a foundation for research into secure logging for federated learning systems under the EU AI Act.

---

## Architecture

```text
Client Request
      │
      ▼
API Service (FastAPI)
  ├── Handles requests
  ├── Generates correlation IDs
  ├── Emits structured JSON logs
  ├── Exposes Prometheus metrics
  └── Forwards audit events asynchronously
      │
      ▼
Logging Service (FastAPI)
  ├── Receives audit events
  ├── Assigns server-side timestamps
  ├── Generates log_id
  └── Stores append-only audit records
      │
      ▼
Append-Only Audit Log
(logging-service/data/audit-log.jsonl)
```

This separation ensures that application services do not directly manipulate audit records.

---

## Deployment Architecture

```text
Developer
   ↓
GitHub Repository
   ↓
GitHub Actions (CI/CD)
   ↓
Docker Hub Registry
   ↓
AWS EC2
   ↓
Docker Compose
   ↓
API Service
Logging Service
Prometheus
```

---

## Current Features

### API Service

The API service provides operational endpoints, structured logging, metrics, and audit-event forwarding.

| Endpoint | Purpose |
|---|---|
| `/health` | Service health check |
| `/status` | Basic service status |
| `/submit` | Simulated event submission |
| `/metrics` | Prometheus metrics endpoint |

Key capabilities:

- Structured JSON logging
- Request correlation via `request_id`
- Middleware-based request logging
- Background audit forwarding
- Prometheus request metrics and latency tracking

---

### Logging Service

The logging service receives and stores structured audit events.

| Endpoint | Purpose |
|---|---|
| `/health` | Logging service health check |
| `/ingest` | Accepts audit events from other services |
| `/logs` | Returns recent stored audit records |

Each stored record contains:

```text
log_id
timestamp
service
request_id
event_name
event_type
payload
```

Events are stored in JSON Lines format (`.jsonl`) using append-only writes.

---

### Prometheus Observability

Prometheus scrapes the API service through the `/metrics` endpoint.

Example metrics include:

```text
api_requests_total
api_request_latency_seconds
```

These metrics provide visibility into:

- Request counts
- Request latency
- Endpoint-level traffic
- Service behaviour over time

---

## Structured Logging Schema

Each request processed by the API service emits structured logs with the following fields:

```text
timestamp
level
service
request_id
method
path
status_code
duration_ms
client_ip
user_agent
```

Endpoint-specific fields may include:

```text
event_type
```

Schema stability matters because schema drift can break dashboards, queries, alerts, and audit validation.

---

## Quickstart: Local Development

### Clone the Repository

```bash
git clone https://github.com/jaymacsberg/secure-audit-logging-platform.git
cd secure-audit-logging-platform
```

### Start the Logging Service

```bash
cd logging-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 9000
```

### Start the API Service

Open another terminal:

```bash
cd api-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Submit an Event

```bash
curl -X POST http://127.0.0.1:8000/submit \
  -H "Content-Type: application/json" \
  -d '{
        "event_type": "demo",
        "message": "hello",
        "metadata": {"source": "quickstart"}
      }'
```

### Verify the Event Was Recorded

```bash
curl http://127.0.0.1:9000/logs?n=5
```

---

## Docker Compose Modes

### Local Development

```text
docker-compose.yml
```

The local Compose file builds containers from source.

Run locally:

```bash
docker compose up --build
```

or, with classic Docker Compose:

```bash
docker-compose up --build
```

---

### Production Deployment

```text
docker-compose.prod.yml
```

The production Compose file pulls prebuilt images from Docker Hub instead of building them locally.

This is used on AWS EC2 for deployment.

---

## AWS EC2 Deployment

The platform has been deployed on an AWS EC2 Ubuntu instance using Docker Compose.

Services running on EC2:

| Service | Port | Purpose |
|---|---|---|
| API Service | `8000` | Main application API |
| Logging Service | `9000` | Audit event ingestion and retrieval |
| Prometheus | `9090` | Metrics monitoring |

Example cloud endpoints:

```text
http://<EC2_PUBLIC_IP>:8000/health
http://<EC2_PUBLIC_IP>:9000/logs?n=5
http://<EC2_PUBLIC_IP>:9090
```

Note: accessing only `http://<EC2_PUBLIC_IP>` will not work unless a reverse proxy or load balancer is configured on port `80`.

---

## CI/CD Pipeline

The platform uses GitHub Actions for continuous integration and deployment.

On every push to the `main` branch:

1. Docker images are built automatically
2. Images are pushed to Docker Hub
3. GitHub Actions connects to AWS EC2 over SSH
4. EC2 pulls the latest images
5. Containers are restarted automatically using `docker-compose.prod.yml`

### CI/CD Workflow

```text
git push
   ↓
GitHub Actions
   ↓
Build Docker images
   ↓
Push images to Docker Hub
   ↓
Deploy to EC2
```

---

## Docker Hub Images

The production deployment pulls images from Docker Hub:

```text
jaymacsberg/secure-api-service:latest
jaymacsberg/secure-logging-service:latest
```

This separates image building from runtime deployment.

The EC2 server acts as a runtime host, while GitHub Actions handles image building and publishing.

---

## Why This Project Exists

Modern AI and healthcare systems require provable traceability of system actions.

A secure audit pipeline should support:

- Consistent event structure
- Centralised event recording
- Traceable request lifecycle
- Operational observability
- Secure and auditable logging foundations

This project demonstrates the foundational architecture required to support such systems.

---

## Progress So Far

### Week 1

- Built API service with structured logging
- Added request correlation IDs
- Implemented middleware-based request logging

### Week 2

- Built dedicated logging microservice
- Added audit event forwarding from API service to logging service
- Implemented append-only JSONL audit storage

### Week 3

- Containerised both services with Docker
- Added Docker Compose for multi-service orchestration
- Externalised service configuration with environment variables

### Week 4

- Added Prometheus metrics instrumentation
- Exposed `/metrics` endpoint
- Added Prometheus scraping through Docker Compose

### Week 5

- Deployed the full platform on AWS EC2
- Installed Docker and Docker Compose on Ubuntu server
- Ran the platform remotely in the cloud
- Verified public API, logging, and Prometheus access

### Week 6

- Added GitHub Actions CI pipeline
- Automated Docker image builds
- Pushed images to Docker Hub
- Added production Compose deployment file
- Implemented automated EC2 deployment from GitHub Actions

---

## Planned Next Steps

- Kubernetes deployment
- Grafana dashboards
- OpenTelemetry tracing
- Tamper-evident audit chains
- Distributed event streaming
- Provenance verification

---

## Author

**Joshua Bolade**
