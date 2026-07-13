PROJECT STATE

Last Updated: 2026-06-28
Project: python-api-docker
Status: Production-like Observability System (Learning Environment)

1. Project Objective

This project is a production-like system designed to practice real-world DevOps and SRE concepts.

It includes:

Docker & Docker Compose
Flask API development
PostgreSQL database
Nginx reverse proxy
Prometheus metrics collection
Grafana dashboards
Logging & monitoring
Observability fundamentals (SRE)
Primary Goal

Build a fully documented system that:

Can be understood without prior context
Can be rebuilt from documentation alone
Mimics real production observability pipelines
2. Current System Architecture
Client
  ↓
Nginx (Reverse Proxy - Port 80)
  ↓
Flask API (Port 5000)
  ↓
PostgreSQL
3. Observability Architecture
Flask API → Custom Metrics (/metrics) → Prometheus → Grafana Dashboards
4. Implemented Components
4.1 Flask API
Endpoints
GET / → Root health response
GET /health → Service status check
GET /db → Database connectivity test
GET /metrics → Prometheus metrics endpoint
Observability Features
Request ID middleware
Request latency tracking
Structured JSON logging
Custom metrics (request rate, latency, errors)
Endpoint-level monitoring
4.2 PostgreSQL
Implementation
PostgreSQL container (Dockerized)
Internal Docker networking
Health checks enabled
Connected to Flask API via /db
Status
Running
Healthy
4.3 Nginx
Role
Reverse proxy (entry point)
Routes traffic to Flask API
Status
Stable and production-like
4.4 Monitoring Stack
Components
Prometheus (metrics collection)
Grafana (visual dashboards)
Flask /metrics exporter
Metrics Available
Request count
Request rate
Latency (response time)
Error rate
Endpoint-level traffic
Status
Prometheus: Running
Grafana: Running
Metrics: Active and scraping
5. System Status Overview
Component    | Status
------------ | -------------
API          | Running (Verified on Port 5000)
Database     | Healthy (Verified connectivity)
Nginx        | Stable (Using default baseline configuration)
Prometheus   | Running & Actively Scraping
Grafana      | Running & Connected to Prometheus Data Source (Verified)
Metrics      | Active (Custom metrics like http_requests_total verified via load test)
6. Known Issues
/db endpoint occasionally unstable (rare)
Middleware sensitive to structural changes
Needs stronger global exception handling

7. Major Lessons Learned
7.1 Middleware Design

Improper middleware ordering causes:

missing request_id
broken request lifecycle
HTTP 500 errors

Rule:
Never refactor Flask core in a single step.

7.2 Nginx Configuration

Incorrect structure causes container crash loops.

Rule:
Use:

nginx/conf.d/default.conf
7.3 Observability Principle

Metrics must evolve alongside the API, not after it.

7.4 Secrets Handling

Never commit sensitive data (tokens, keys, credentials).

7.5 Prometheus Scraping Behavior:** Changes in application endpoints (like `/db`) aren't reflected instantly; they adhere to the defined `scrape_interval` (5s).

7.6 Metric Typology:** Standard container health metrics (`up`) only show binary status (0 or 1), whereas custom counters (`http_requests_total`) are required to track actual traffic behavior.
8. Technical Debt
Improve /db robustness
Add global exception handler
Standardize logging format
Strengthen middleware reliability
9. Future Enhancements
Alertmanager integration (alerting layer)
Loki logging stack
OpenTelemetry tracing
CI/CD with GitHub Actions
Kubernetes deployment
Blue/Green deployment strategy
Automated backups
10. Next Step (System Evolution)

The system is now in a fully observable state.

Next phase:

Alerting + Advanced Dashboards

Suggested direction:

Grafana dashboards (latency / error rate / request rate)
Alert rules (Prometheus Alertmanager)
SLO / SLI definition
11. Documentation Rule

This file is the single source of truth.

Always check before changes:

PROJECT_STATE.md
ARCHITECHURE.md
RUNBOOK.md


12. Current Known Good State

Windows 11
Docker Desktop
WSL2 Ubuntu
Docker Compose v2
Registry Mirror configured
All containers running successfully

13. Major Lessons Learned

Docker Hub access may fail because of DNS/routing restrictions.
Docker Registry Mirror can completely eliminate Docker Hub connectivity issues without modifying project files.
Windows + WSL2 provides a stable development environment for the project.
