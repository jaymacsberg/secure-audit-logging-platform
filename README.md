# Secure Audit Logging and Observability Platform
This project is a hands-on backend, logging, and observability project focused on building a secure audit-event service with structured logging, request tracing, containerised deployment, and Kubernetes practice.

The project demonstrates practical work with FastAPI, Python, Docker, Docker Compose, Kubernetes manifests, GitHub Actions, structured JSON logs, health/status endpoints, and request-level traceability.
This repository is presented as a learning and research-aligned engineering project, not as a live production system.
---
## Project Objectives
* Build an API service for receiving and validating audit events
* Implement structured JSON logging for easier troubleshooting and traceability
* Add UUID-based request IDs to correlate requests across logs
* Provide health and status endpoints for operational visibility
* Containerise services using Docker and Docker Compose
* Deploy workloads using Kubernetes manifests
* Use GitHub Actions for validation checks
* Document system behaviour, testing steps, and troubleshooting notes
---

## Technologies Used
* Python
* FastAPI
* Uvicorn
* Docker
* Docker Compose
* Kubernetes
* GitHub Actions
* Bash
* curl
* jq
* JSON
* Structured logging
* Prometheus / observability concepts
---
## Core Features
* Audit-event submission endpoint
* Health-check endpoint
* Status endpoint
* Structured JSON logging
* UUID request correlation
* Logging middleware
* Containerised API service
* Separate event/log processing component
* Kubernetes workload and service definitions
* CI/CD validation workflow using GitHub Actions
---

## Repository Structure
```text
secure-audit-logging-platform/
├── .github/workflows/      # GitHub Actions validation workflows
├── api/                    # FastAPI service code
├── logging-service/        # Event/log processing service
├── kubernetes/             # Kubernetes manifests
├── prometheus/             # Monitoring or metrics configuration
├── docker-compose.yml      # Local multi-service deployment
├── README.md               # Project documentation
└── ...
```

---

## API and Logging Overview

The platform includes an API service that accepts structured audit events and records request-level activity using structured logs.

The logging design focuses on:

* Capturing request metadata
* Correlating requests using UUID request IDs
* Producing JSON-formatted logs
* Supporting easier debugging and traceability
* Providing operational endpoints for health and status checks

---

## Local Development

A typical local workflow includes:

1. Create and activate a Python virtual environment
2. Install project dependencies
3. Run the FastAPI service locally with Uvicorn
4. Test health and status endpoints
5. Submit sample audit events using `curl`
6. Inspect structured JSON logs
7. Run the service stack using Docker Compose
8. Validate container behaviour and service responses

Example local test commands:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/status
```

---

## Container and Kubernetes Practice

The project includes containerisation and Kubernetes deployment practice through:

* Dockerfiles for service packaging
* Docker Compose for local multi-service testing
* Kubernetes manifests for workload deployment
* Service definitions for exposing workloads
* Validation of pod and service behaviour

---

## CI/CD and Validation
GitHub Actions is used to support automated validation checks.

Validation activities include:

* Checking project structure
* Running basic build or syntax checks
* Validating repeatable project setup
* Supporting safer changes through automated workflows

---

## Troubleshooting and Observability

The project supports troubleshooting practice through:

* Health and status endpoints
* Structured logs
* Request IDs
* API response testing
* Container logs
* Kubernetes workload inspection
* Basic monitoring and observability concepts

Useful troubleshooting commands include:

```bash
docker compose ps
docker compose logs
kubectl get pods
kubectl get services
kubectl logs <pod-name>
```

---

## Research Context

This project is aligned with broader research interests in secure logging, auditability, model provenance, distributed systems, and traceability.

The implementation is intentionally practical and engineering-focused, with emphasis on how logs, request IDs, validation endpoints, and deployment evidence can support system reliability and review.

---

## Security and Repository Hygiene

This repository should not contain credentials, private keys, `.env` files, API secrets, database passwords, kubeconfig files, or cloud credentials.

Sensitive runtime values should be handled through environment variables, local configuration, GitHub repository secrets, or secure deployment tooling.

---

## Status

Active learning and research-aligned engineering project.

The system may continue to evolve as additional logging, monitoring, deployment, and validation features are added.

---

## Career Relevance

This project demonstrates practical skills relevant to application support, production support, cloud support, DevOps, platform support, and observability-focused roles, including:

* API troubleshooting
* Structured logging
* Request tracing
* Health-check design
* Docker-based deployment
* Kubernetes deployment practice
* CI/CD validation
* Technical documentation
* Debugging and operational thinking
