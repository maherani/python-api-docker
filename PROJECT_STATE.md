# PROJECT STATE

Last Updated: 2026-06-22

---

# Project Name

python-api-docker

---

# Objective

Build a production-like platform for learning and practicing:

- Docker
- Docker Compose
- Nginx Reverse Proxy
- Flask API
- PostgreSQL
- Observability
- Prometheus
- Grafana
- Logging
- Monitoring
- SRE Concepts

Primary goal:

Create a fully documented environment that can be understood, operated, and extended by a new developer (or future ChatGPT session) without prior knowledge.

---

# Current Architecture

Client
↓
Nginx (Port 80)
↓
Flask API (Port 5000)
↓
PostgreSQL

Metrics pipeline:

API → Prometheus → Grafana

---

# Implemented Features

## API

Implemented endpoints:

- GET /
- GET /health
- GET /db
- GET /metrics

Observability:

- request_id generation (middleware-based)
- request latency calculation
- structured JSON logging

Example log:

```json
{
  "request_id": "test-1",
  "path": "/",
  "method": "GET",
  "status": 200,
  "latency_ms": 0.03
}

Status:

Running
Healthy (with known intermittent DB error risk)
Database

Implemented:

PostgreSQL 16 container
Internal Docker network access
Health checks enabled

Status:

Running
Healthy

Note:

/db endpoint previously experienced intermittent 500 errors due to application-level exception handling issues.

Nginx

Implemented:

Reverse proxy
Routing to Flask API

Status:

Stable (after fixing crash loop issue)

Known Incident:

Wrong nginx configuration caused restart loop.

Error:

server directive is not allowed here

Resolution:

Root nginx.conf must not contain server block
Use:
nginx/conf.d/default.conf
Monitoring

Implemented:

Prometheus container
Grafana container
/metrics endpoint in API

Status:

Infrastructure deployed
Scraping validation: pending
Grafana dashboard: not yet created
Repository Status

Repository:

python-api-docker

Branch:

main

Documentation:

README.md
docs/ARCHITECHURE.md
docs/RUNBOOK.md
docs/PROJECT_STATE.md
Major Lessons Learned
1. Logging Middleware Bug (Critical Incident)

Issue:

request.request_id missing
request.start_time missing
caused HTTP 500 errors

Root Cause:

Middleware was removed or not initialized before request lifecycle.

Resolution:

Restored middleware
Fixed incremental change approach

Rule:

Never rewrite working Flask app fully. Apply incremental changes only.

2. Nginx Misconfiguration (Critical Incident)

Issue:

nginx container restart loop

Error:

server directive is not allowed here

Root Cause:

Wrong nginx.conf structure

Resolution:

Move server block to:
nginx/conf.d/default.conf

Rule:

Do not replace full nginx root config unless necessary.

3. GitHub Push Protection Incident

Issue:

Personal Access Token committed accidentally

Impact:

Git push blocked (GH013 rule violation)

Resolution:

Removed secret file
Cleaned commit history
Added .gitignore rules

Rule:

Never store secrets in repository.

Current Known Good State

Expected containers:

nginx_proxy
python_api
db
prometheus
grafana

Validation:

docker-compose ps

Expected:

nginx_proxy → Up
python_api → Up (healthy)
db → Up (healthy)
prometheus → Up
grafana → Up
Verified Working Features
API
curl http://localhost/

Expected: HTTP 200

curl http://localhost/health

Expected:

{
  "status": "ok"
}
curl http://localhost/db

Status:

Works
But previously observed intermittent 500 (needs stabilization review)
curl http://localhost/metrics

Expected:

Prometheus metrics output

Logging

Verified structured JSON logs:

{
  "request_id": "test-1",
  "path": "/",
  "method": "GET",
  "status": 200,
  "latency_ms": 0.03
}
Pending Work
High Priority
Validate Prometheus scraping stability
Validate Grafana datasource connection
Create first dashboard
Medium Priority
Request count dashboard
Latency dashboard
Error rate dashboard
Technical Debt
Stabilize /db endpoint error handling
Improve middleware robustness
Add global exception handler
Future Enhancements
GitHub Actions CI/CD
Alertmanager
Loki logging stack
OpenTelemetry tracing
Distributed tracing
Kubernetes deployment
Blue/Green deployment
Automated backup strategy
Next Recommended Step

Complete observability validation:

API → Metrics → Prometheus → Grafana

Success criteria:

Prometheus scraping OK
Grafana datasource connected
Dashboard shows live API metrics
Notes For Future Sessions

This file is the single source of truth for project state.

Any new session should start by reading:

PROJECT_STATE.md
ARCHITECHURE.md
RUNBOOK.md

These define:

System architecture
Operational behavior
Known incidents
Current stability level
Next engineering steps
