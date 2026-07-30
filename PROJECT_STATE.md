# PROJECT STATE
**Last Updated:** 2026-07-29
**Project:** python-api-docker
**Status:** Production-Grade SRE & Observability Environment

## 1. Project Objective
This project is engineered as a production-like system designed to practice real-world DevOps, Site Reliability Engineering (SRE), and Infrastructure as Code (IaC) concepts. 
Primary goals include building a resilient Hub-and-Spoke Git workflow, managing containerized microservices, enforcing configuration management with Ansible, and maintaining a robust observability pipeline.

## 2. Current System Architecture
[cite_start]The system follows a strict decoupled architecture to enforce security boundaries and scalability[cite: 257, 258]:

* [cite_start]**Git Workflow:** Hub-and-Spoke architecture (Local GitLab syncing to Central GitHub via Repository Mirroring)[cite: 205, 208].
* [cite_start]**CI/CD:** Local GitLab Runner bound to the host `docker.sock` for automated deployments[cite: 218].
* [cite_start]**Edge Layer:** Nginx acting as a reverse proxy with IP-based rate limiting (10 requests/second) on port 80[cite: 254, 280].
* [cite_start]**Application Layer:** Replicated Flask API running on internal port 5000[cite: 254, 275].
* [cite_start]**Data Tier:** Isolated PostgreSQL 16 database operating securely within the internal Docker network on port 5432[cite: 257, 275].

## 3. Observability Matrix
[cite_start]An "Observability-First" design is deeply integrated into the system, avoiding post-deployment monitoring patches[cite: 259]:

* [cite_start]**Grafana Alloy:** Replaces older agents to act as a unified collector, processing logs and telemetry from the Docker socket[cite: 160, 278].
* [cite_start]**Prometheus & Exporters:** Scrapes metrics actively from the Flask API (`/metrics`), `node-exporter` (hardware), and `postgres-exporter`[cite: 251, 278, 279].
* [cite_start]**Grafana Loki:** Receives structured JSON logs directly from Alloy for aggregation and querying[cite: 277, 278].
* [cite_start]**Alertmanager:** Evaluates critical thresholds (e.g., API replicas down, High CPU, DB down) and routes alerts to a Telegram Bot[cite: 231, 267, 268, 270].
* [cite_start]**Grafana:** Visualizes the complete stack using pre-provisioned data sources[cite: 277].

## 4. Implemented Components & API Endpoints

| Endpoint | Method | Purpose |
| :--- | :--- | :--- |
| `/` | `GET` | [cite_start]Root confirmation and latency check[cite: 239]. |
| `/health` | `GET` | [cite_start]Infrastructure validation layer[cite: 240]. |
| `/db` | `GET` | [cite_start]Structural upstream database connection test[cite: 240]. |
| `/users` | `POST` | [cite_start]Creates a new user record in the database via JSON[cite: 239]. |
| `/slow` | `GET` | [cite_start]Simulates a 3-second downstream resource starvation[cite: 240]. |
| `/error` | `GET` | [cite_start]Simulates standard HTTP 500 server exception[cite: 241]. |
| `/metrics` | `GET` | [cite_start]Exposes Prometheus telemetry records[cite: 241]. |

## 5. System Status Overview

| Component | Status | Verification Method |
| :--- | :--- | :--- |
| **API** | Stable | [cite_start]Returns active HTTP 200 on `/health` and `/`[cite: 239, 240]. |
| **Database** | Stable | [cite_start]PostgreSQL accepts internal overlay connections[cite: 257]. |
| **Nginx** | Active | [cite_start]Routes traffic to API and applies rate limits[cite: 254, 280]. |
| **Prometheus** | Scraping | [cite_start]Collecting from `app`, `node-exporter`, and `postgres-exporter`[cite: 251]. |
| **Alertmanager** | Active | [cite_start]Telegram routing configured and ready[cite: 231]. |
| **Ansible (IaC)** | Provisioned | [cite_start]Server setup playbooks validated[cite: 264]. |

## 6. Major Lessons Learned & Technical Debt

* [cite_start]**Permission Denied Faults:** Prometheus (UID 65534) and Loki (UID 10001) execute under unprivileged security profiles[cite: 195]. [cite_start]Volume mappings require explicit host-level ownership adjustments via Ansible or manual `chown`[cite: 196].
* [cite_start]**Network Interruptions (WSL2):** Dynamic network interruptions in Windows 11 cause Docker Hub pulling failures[cite: 188]. [cite_start]Remediation requires mapping virtual network configurations via `.wslconfig`[cite: 189, 192].
* [cite_start]**Middleware Design:** Improper middleware ordering causes missing `request_id` and broken request lifecycles (HTTP 500 errors)[cite: 262].
* [cite_start]**Dependency Management:** Deploying without version pinning in `requirements.txt` introduces severe instability[cite: 126]. [cite_start]Exact versions must always be locked[cite: 127].

## 7. Next Steps (System Evolution)
The system has achieved a highly observable state with IaC foundations. Suggested next phases:
* Implement Trivy for automated Docker image vulnerability scanning (SecOps integration).
* Implement Bandit for Python static application security testing (SAST).
* Explore horizontal scaling with Kubernetes orchestration.
* Establish secure Secrets Management (e.g., HashiCorp Vault) to replace `.env` file dependencies.

## 8. Documentation Rule
This file is the single source of truth. Always check before changes:
1. `PROJECT_STATE.md`
2. `ARCHITECTURE.md`
3. `RUNBOOK.md`
