# System Architecture — Python API Docker Platform

## Overview

This system is a containerized microservice architecture designed for learning **production-grade SRE patterns**, including:

- Reverse proxy routing
- Service isolation
- Observability pipeline
- Database separation
- Metrics collection

---

## High-Level Architecture

Client
↓
Nginx (Reverse Proxy - Port 80)
↓
Flask API (Internal Service - Port 5000)
↓
PostgreSQL (Internal Database)

Observability Flow:

Flask API → Prometheus → Grafana

---

## Component Breakdown

## 1. Nginx (Edge Layer)

Role:

- Entry point of the system
- Reverse proxy
- Routes traffic to internal API service

Configuration:

- Listens on port 80
- Proxies requests to `python_api:5000`

Important Constraint:

Nginx must NOT contain full application configuration inside `nginx.conf`.

Correct structure:


nginx/
└── conf.d/
└── default.conf


---

## 2. Flask API (Application Layer)

Role:

Core backend service

Responsibilities:

- Business logic
- Request handling
- Database communication
- Metrics exposure

Endpoints:

- `/` → Base endpoint
- `/health` → Health check
- `/db` → DB connectivity test
- `/metrics` → Prometheus metrics

Observability:

- request_id middleware
- request latency tracking
- structured logging

---

## 3. PostgreSQL (Data Layer)

Role:

- Persistent data storage
- Internal-only service

Configuration:

- Not exposed externally
- Accessible only via Docker network

---

## 4. Prometheus (Metrics Layer)

Role:

- Scrapes metrics from Flask API
- Collects system-level observability data

Target:

- `/metrics` endpoint

---

## 5. Grafana (Visualization Layer)

Role:

- Dashboard visualization
- Metrics exploration
- System monitoring

Current Status:

- Deployed
- Dashboard creation pending

---

## Data Flow

### Request Flow

Client Request
→ Nginx
→ Flask API
→ PostgreSQL (if needed)
→ Response

---

### Metrics Flow

Flask API
→ Prometheus scraping
→ Grafana dashboards

---

## Network Design

All services run inside Docker network:

app_network

Internal communication:

- nginx → api:5000
- api → db:5432

---

## Key Design Decisions

### 1. Reverse Proxy Isolation

Nginx is the only public entry point.

Reason:

- security boundary
- traffic control
- future scalability

---

### 2. Internal Database Isolation

PostgreSQL is not exposed externally.

Reason:

- prevent direct access
- enforce service-layer access only

---

### 3. Observability First Design

Metrics are built into API from early stage.

Includes:

- request duration
- request identity
- structured logs

---

## Known Issues / Incidents

### 1. Nginx Misconfiguration Incident

Problem:

Incorrect nginx.conf structure caused container restart loop.

Error:

```text id="nginx_err"
server directive is not allowed here

Root Cause:

Wrong placement of server block

Fix:

Move configuration to:

nginx/conf.d/default.conf
2. Application Middleware Issue

Problem:

request_id missing
start_time missing
resulted in HTTP 500 errors

Root Cause:

Middleware not initialized correctly

Fix:

Incremental restoration of working version

Scalability Considerations

Current limitations:

Single API instance
No load balancing
No horizontal scaling

Future improvements:

Kubernetes deployment
API replicas behind Nginx
Redis caching layer
Observability Strategy

Current stack:

Prometheus (metrics collection)
Grafana (visualization)
Flask /metrics endpoint

Planned additions:

Alertmanager (alerting)
Loki (logs aggregation)
OpenTelemetry (distributed tracing)
Security Model
Only Nginx exposed externally
Database internal-only
No secrets stored in repository
.gitignore enforced for sensitive files
System Philosophy

This system is designed with:

simplicity first
observability by default
failure transparency
incremental evolution (not big rewrites)
Dependency Graph

Nginx
↓
Flask API
↓
PostgreSQL

Flask API
↓
Prometheus
↓
Grafana

Summary

This architecture simulates a real production environment with:

reverse proxy layer
backend service layer
database layer
observability stack

It is intended for:

learning SRE concepts
practicing DevOps workflows
simulating production debugging scenarios
