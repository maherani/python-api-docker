README.md (Production-Grade)
# Python API Docker Platform

A production-like containerized system for learning and practicing **DevOps, Docker, and SRE concepts**.

---

## Overview

This project simulates a real-world backend system with full observability, including:

- Flask API (backend service)
- PostgreSQL (database)
- Nginx (reverse proxy)
- Prometheus (metrics collection)
- Grafana (visual dashboards)
- Docker Compose (orchestration)

The goal is to build a system that behaves like a production environment and supports debugging, monitoring, and scaling practices.

---

## Architecture

### System Flow
Client → Nginx → Flask API → PostgreSQL

### Observability Flow
Flask API → Prometheus → Grafana

---

## Features

### API Service

- REST API built with Flask
- Endpoints:
  - `GET /` → Base response
  - `GET /health` → Health check
  - `GET /db` → Database connectivity test
  - `GET /metrics` → Prometheus metrics

### Observability

- Request ID tracking
- Request latency measurement
- Structured JSON logging
- Custom metrics:
  - Request count
  - Request rate
  - Error rate
  - Latency per endpoint

---

### Database

- PostgreSQL containerized
- Internal Docker network only
- Health checks enabled

---

### Reverse Proxy

- Nginx as entry point
- Routes traffic to Flask API
- Isolated configuration (`conf.d/default.conf`)

---

### Monitoring Stack

- Prometheus → metrics collection
- Grafana → dashboards & visualization

---

## Tech Stack

- Python (Flask)
- PostgreSQL
- Nginx
- Docker & Docker Compose
- Prometheus
- Grafana

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/your-username/python-api-docker.git
cd python-api-docker

2. Start System
docker-compose up --build -d

3. Check Services
docker-compose ps

Expected:

  nginx_proxy → Up
  python_api → Up (healthy)
  db → Up (healthy)
  prometheus → Up
  grafana → Up

4. Test API
  curl http://localhost/
  curl http://localhost/health
  curl http://localhost/db
  curl http://localhost/metrics

Monitoring
Prometheus
  URL: http://localhost:9090
  Targets: /metrics

Grafana
  URL: http://localhost:3000
  Default dashboards: (to be configured)

Observability Features
  Request tracing via request_id
  Endpoint latency tracking
  Error rate tracking
  Metrics exposed via /metrics

Known Issues
  /db endpoint may occasionally show intermittent errors
  Middleware is sensitive to structural changes
  Grafana dashboards require manual setup

System Design Principles
  Simplicity first
  Observability by default
  Incremental changes (no full rewrites)
  Production-like architecture simulation

Architecture Diagram
    Client
      ↓
    Nginx (Port 80)
      ↓
    Flask API (Port 5000)
      ↓
    PostgreSQL

Observability Pipeline
  Observability Pipeline

Future Improvements
  Alertmanager integration
  Loki logging stack
  OpenTelemetry tracing
  CI/CD pipeline (GitHub Actions)
  Kubernetes deployment
  Horizontal scaling (API replicas)
  Blue/Green deployment
Lessons Learned
  Middleware order is critical in Flask applications
  Nginx misconfiguration can crash the reverse proxy layer
  Observability should be integrated early, not added later
  Secrets must never be stored in the repository
Project Status

  This project is currently in:

  Observability & Monitoring Phase (Production-like System)

Author Notes
  This system is designed as a learning environment for:

  DevOps engineering
  SRE fundamentals
  Backend system design
  Observability pipelines

It is intentionally structured to simulate real-world production issues and debugging workflows.


Docker Registry Mirror Configuration

Problem:
Docker Hub may not be reachable in some networks due to DNS or routing restrictions.

Solution:

Docker Desktop
Settings
→ Docker Engine

{
  ...
  "registry-mirrors": [
    "https://docker-mirror.liara.ir"
  ]
}

Apply & Restart

Verification:

docker pull postgres:16
docker pull nginx:alpine
docker pull prom/prometheus:latest


If all images are pulled successfully, the mirror is configured correctly.
