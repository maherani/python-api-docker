# PROJECT_STATE.md

## Project Overview

This is a learning DevOps project built with:

* Flask
* PostgreSQL
* Docker
* Docker Compose
* Nginx Reverse Proxy
* GitHub

The purpose of this project is to learn practical DevOps concepts step by step.

---

## Current Status

### Infrastructure

Running services:

* nginx_proxy
* python_api
* postgres

Container status:

* nginx_proxy: healthy
* python_api: healthy
* postgres: healthy

---

## Implemented Features

### API Endpoints

GET /

Returns welcome response.

GET /health

Returns application health status.

GET /db

Tests PostgreSQL connectivity.

---

### Logging

Implemented:

* JSON structured logging
* Request ID support
* Latency measurement
* Method, path and status logging

Example:

{
"request_id": "test-1",
"path": "/",
"method": "GET",
"status": 200,
"latency_ms": 0.03
}

---

### Reverse Proxy

Nginx is the only exposed service.

Exposed Port:

* 80

Internal services:

* Flask: 5000
* PostgreSQL: 5432

Flask is not exposed directly to the host.

---

## Git Information

Repository:

[git@github.com](mailto:git@github.com):maherani/python-api-docker.git

Default Branch:

main

---

## Problems Already Solved

### Docker Permission

Solved by:

sudo usermod -aG docker $USER
newgrp docker

---

### GitHub SSH Access

SSH port 22 is blocked in company network.

Current workaround:

HTTPS remote URL

---

### Secret Scanning Incident

A GitHub PAT was accidentally committed.

Actions:

* removed from git history
* added to .gitignore
* repository cleaned

Future rule:

Never store tokens inside repository files.

---

## Next Planned Phase

Priority 1:

Prometheus Metrics

Tasks:

* add prometheus_client
* create /metrics endpoint
* expose metrics through nginx

Priority 2:

Grafana Dashboard

Tasks:

* add Grafana container
* visualize request count
* visualize latency

Priority 3:

GitHub Actions CI/CD

Tasks:

* lint
* build
* docker image build
* automatic deployment

---

## Known Decisions

Decision 001:

Application logs must be JSON structured.

Decision 002:

Only Nginx is exposed externally.

Decision 003:

Database is accessible only from internal Docker network.

Decision 004:

Project focuses on learning DevOps incrementally.

---

## Last Verified State

Date:

2026-06-22

Verified By:

Rasoul

Result:

Application working correctly through Nginx.
Health endpoint operational.
Database endpoint operational.
Structured logging operational.
GitHub repository synchronized.
