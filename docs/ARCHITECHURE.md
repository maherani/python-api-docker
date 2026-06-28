SYSTEM ARCHITECTURE — Python API Docker Platform

Project: python-api-docker
Layer: Production-like SRE Learning System
Version: 2026-06-28

1. Overview

This system is a containerized microservice architecture designed to simulate production-grade SRE patterns.

It includes:

Reverse proxy routing
Service isolation
Observability pipeline
Database separation
Metrics collection
2. High-Level Architecture
Client
  ↓
Nginx (Reverse Proxy - Port 80)
  ↓
Flask API (Internal Service - Port 5000)
  ↓
PostgreSQL (Internal Database)
3. Observability Flow
Flask API → Prometheus → Grafana
4. Component Breakdown
4.1 Nginx (Edge Layer)
Role
Entry point of system
Reverse proxy
Traffic routing to API
Configuration Constraint

Nginx must NOT contain full application config in nginx.conf.

Correct Structure
nginx/
└── conf.d/
    └── default.conf
Routing
External traffic → nginx:80
Internal → python_api:5000
4.2 Flask API (Application Layer)
Role

Core backend service

Responsibilities
Business logic
Request handling
Database communication
Metrics exposure
Endpoints
GET / → Base endpoint
GET /health → Health check
GET /db → Database test
GET /metrics → Prometheus metrics
Observability Features
request_id middleware
request latency tracking
structured logging
4.3 PostgreSQL (Data Layer)
Role
Persistent storage
Internal-only service
Security Model
Not exposed externally
Accessible only via Docker network
4.4 Prometheus (Metrics Layer)
Role
Scrapes metrics from Flask API
Collects system observability data
Target
/metrics endpoint
4.5 Grafana (Visualization Layer)
Role
Dashboard visualization
Metrics exploration
System monitoring
Status
Deployed
Dashboards: pending refinement
5. Data Flow
5.1 Request Flow
Client → Nginx → Flask API → PostgreSQL → Response
5.2 Metrics Flow
Flask API → Prometheus → Grafana
6. Network Design

All services run inside Docker network:

app_network
Internal Communication
nginx → python_api:5000
api → db:5432
7. Key Design Decisions
7.1 Reverse Proxy Isolation

Only Nginx is exposed externally.

Reason:

Security boundary
Traffic control
Scalability foundation
7.2 Database Isolation

PostgreSQL is not publicly exposed.

Reason:

Prevent direct access
Enforce service-layer access
7.3 Observability First Design

Metrics are built into API from early stage.

Includes:

Request duration
Request identity
Structured logs
8. Known Issues & Incidents
8.1 Nginx Misconfiguration Incident (Critical)
Problem

Invalid nginx configuration caused container restart loop.

Error
server directive is not allowed here
Root Cause

Server block placed in wrong configuration file.

Fix

Move configuration to:

nginx/conf.d/default.conf
8.2 Middleware Failure Incident (Critical)
Problem
request_id missing
start_time missing
HTTP 500 errors
Root Cause

Middleware not properly initialized in request lifecycle

Fix

Incremental restoration (no full rewrite)

9. Scalability Considerations
Current Limitations
Single API instance
No load balancing
No horizontal scaling
Future Improvements
Kubernetes deployment
API replicas behind Nginx
Redis caching layer
10. Observability Strategy
Current Stack
Prometheus (metrics)
Grafana (dashboards)
Flask /metrics
Planned Extensions
Alertmanager (alerts)
Loki (logs aggregation)
OpenTelemetry (tracing)
11. Security Model
Only Nginx exposed externally
Database internal-only
No secrets stored in repository
.gitignore enforced
12. System Philosophy

This system is designed with:

Simplicity first
Observability by default
Failure transparency
Incremental evolution (no big rewrites)
13. Dependency Graph
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
14. Summary

This architecture simulates a real production environment:

Reverse proxy layer (Nginx)
Application layer (Flask)
Data layer (PostgreSQL)
Observability stack (Prometheus + Grafana
