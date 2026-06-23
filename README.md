# Python API Docker Platform

## Overview

This project is a containerized microservice system designed for learning and practicing **real-world SRE and DevOps concepts**.

It includes:

- Flask API (backend service)
- PostgreSQL (database)
- Nginx (reverse proxy)
- Prometheus (metrics)
- Grafana (monitoring & dashboards)

---

## Architecture

Client
↓
Nginx (Port 80)
↓
Flask API (Port 5000)
↓
PostgreSQL

Observability Flow:

API → Prometheus → Grafana

---

## Features

### API Service

Endpoints:

- `GET /` → Main endpoint
- `GET /health` → Health check
- `GET /db` → Database connectivity test
- `GET /metrics` → Prometheus metrics

Observability features:

- request_id per request
- request latency tracking (ms)
- structured JSON logging

---

### Database

- PostgreSQL 16 container
- Internal Docker network only
- Health checks enabled

---

### Nginx Reverse Proxy

- Single entry point (port 80)
- Routes traffic to Flask API

⚠️ Important Note:

Correct configuration must be placed in:


nginx/conf.d/default.conf


Do NOT replace full nginx.conf root file.

---

### Monitoring Stack

- Prometheus collects metrics from API
- Grafana visualizes metrics
- /metrics endpoint exposed by Flask

---

## Quick Start

```bash
docker-compose up --build -d
Verify System
docker-compose ps

Expected:

nginx_proxy → Up
python_api → Up (healthy)
db → Up (healthy)
prometheus → Up
grafana → Up
Test Endpoints
Health Check
curl http://localhost/health

Expected:

{
  "status": "ok"
}
Database Test
curl http://localhost/db
Metrics
curl http://localhost/metrics
Known Issues
Intermittent 500 Error on /db

Cause:

Application-level exception handling issue
Needs stabilization in DB error handling
Nginx Misconfiguration History

Issue:

server directive used in wrong context

Error:

server directive is not allowed here

Fix:

Use nginx/conf.d/default.conf
Observability
Prometheus scraping enabled
Grafana dashboard available (setup pending)
Development Workflow

Before pushing changes:

Update code
Update documentation if needed
Run system tests
Commit changes
Push to GitHub
git add .
git commit -m "update"
git push origin main
Future Improvements
CI/CD with GitHub Actions
Centralized logging (Loki)
Distributed tracing (OpenTelemetry)
Alerting system (Alertmanager)
Kubernetes deployment
Goal of This Project

This project is designed to simulate a real production SRE environment, including:

service reliability
observability
failure handling
infrastructure debugging
Documentation
RUNBOOK: docs/RUNBOOK.md
ARCHITECTURE: docs/ARCHITECHURE.md
PROJECT STATE: docs/PROJECT_STATE.md
