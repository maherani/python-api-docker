### Component & Data Traffic Flow
```text
[ Client Requests ]
       │
       ▼
 ┌───────────┐
 │   Nginx   │ (Reverse Proxy - Port 80)
 └─────┬─────┘
       │
       ▼
 ┌───────────┐       ┌────────────┐
 │ Flask API │ ─────►│ PostgreSQL │ (Isolated Network DB)
 └─────┬─────┘       └────────────┘
       │ (Exposes JSON Logs & /metrics)
       ▼
 ┌───────────────┐
 │ Grafana Alloy │ (Central Telemetry Scraping/Forwarding Engine)
 └──────┬────────┘
        ├──────────────────────────────┐
        ▼                              ▼
 ┌───────────────┐              ┌──────────────┐
 │  Prometheus   │ (TSDB)       │ Grafana Loki │ (Log Aggregation)
 └──────┬────────┘              └──────┬───────┘
        │                              │
        └──────────────┬───────────────┘
                       ▼
               ┌──────────────┐       ┌────────────────┐
               │   Grafana    │ ─────►│  Alertmanager  │
               └──────────────┘       └───────┬────────┘
                                              │ (Rule Evaluation Triggers)
                                              ▼
                                      [ Telegram Bot Alert ]
```
# Python API Dockerization & Infrastructure

[cite_start]A production-like, fully containerized system engineered for hands-on learning, development, and practice of DevOps Engineering, Site Reliability Engineering (SRE), and Observability Architectures[cite: 213]. [cite_start]This repository simulates real-world backend infrastructure patterns, system-design constraints, and modern debugging workflows[cite: 213].

---

## 🏛️ System Architecture

### 1. Hub-and-Spoke Git Workflow & CI/CD
[cite_start]To ensure high availability and continuous integration, we utilize a Hub-and-Spoke version control architecture[cite: 191]:
* [cite_start]**Local GitLab (Port 8929):** Developers push their code directly to our internal Dockerized GitLab server at `http://localhost:8929` (or the LAN IP)[cite: 199].
* [cite_start]**Authentication:** Password-based pushes are disabled; developers must use a GitLab Personal Access Token for authentication[cite: 192].
* [cite_start]**Repository Mirroring:** Once code is pushed locally, the internal GitLab automatically mirrors the repository to the central GitHub repository (Single Source of Truth) in the background[cite: 193, 194].
* [cite_start]**GitLab Runner:** A dedicated runner hooked to the host's `docker.sock` automatically triggers the `.gitlab-ci.yml` pipeline upon pushes to the `production` branch, enabling it to build and manage actual project containers[cite: 201, 203, 204].

### 2. Infrastructure as Code (IaC)
[cite_start]Server provisioning and application deployment are fully automated using Ansible[cite: 46]. [cite_start]Playbooks located in the `ansible/` directory manage base environment setups (installing Docker, configuring networks) and deploying the containerized stack[cite: 47, 214, 217].

### 3. Observability & Monitoring Stack
[cite_start]The system is built with an "Observability-First" design[cite: 228]:
* [cite_start]**Prometheus & Exporters:** Scrapes metrics from the Flask API (`/metrics`), Postgres (`postgres-exporter`), and host hardware (`node-exporter`)[cite: 261].
* [cite_start]**Grafana Alloy & Loki:** Alloy acts as a unified collector mapping to the Docker socket to process and pipeline JSON-structured application logs directly to Loki[cite: 43, 212].
* [cite_start]**Alertmanager:** Evaluates continuous thresholds defined in `alerts.yml` (e.g., API replicas down, High CPU, Postgres down) and routes critical alerts to a Telegram Bot channel[cite: 45, 219, 248, 251, 253].
* [cite_start]**Grafana:** Visualizes dynamic dashboards using provisioned data sources (Loki & Prometheus)[cite: 243].

---

## 🛠️ Technology Stack

* [cite_start]**Core Backend:** Python 3.11-slim with Flask[cite: 221, 233].
* [cite_start]**Data Tier:** PostgreSQL 16[cite: 241].
* [cite_start]**Gateway Layer:** Nginx (Alpine Base) serving as a decoupled reverse proxy on Port 80[cite: 242].
* [cite_start]**Orchestration:** Docker & Docker Compose v2[cite: 241].
* [cite_start]**Observability:** Prometheus, Grafana Loki, Grafana Alloy, Alertmanager[cite: 242, 243, 244].

---

## 🚀 Quick Start & Deployment

### 1. Environment Preparation
[cite_start]Before instantiating the cluster, a root-level `.env` file must be provisioned[cite: 62]. [cite_start]Never commit this file or raw secrets to source control[cite: 63].
Required variables:
```ini
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_NAME=postgres

2. Launching the Infrastructure
To spin up the complete architecture in detached mode, run:
docker compose up --build -d


3. Resolving Permission Constraints (Important)
Prometheus and Loki execute under unprivileged security profiles to emulate secure production systems. If you encounter [error opening dir] or Permission Denied in the container logs, modify the host-level directory ownership:

# Set ownership for Prometheus (UID 65534) and Loki (UID 10001)
sudo chown -R 65534:65534 ./prometheus_data
sudo chown -R 10001:10001 ./loki_data

(Note: This step is automatically handled if you deploy using the provided Ansible playbooks ).  

📡 API Endpoints Reference
The core Flask API exposes several structured RESTful endpoints:  

Endpoint,Method,Description
/,GET,Base routing and health response (returns active latency).
/health,GET,Infrastructure validation and service status check.
/db,GET,Structural upstream database connection test.
/users,POST,Creates a new user record in the database via JSON payload.
/slow,GET,Simulates a 3-second downstream resource starvation latency.
/error,GET,Simulates a standard HTTP 500 Internal Server Error.
/metrics,GET,Exposes numerical telemetry records to Prometheus.

🛡️ Git Workflow (How to Push Code)
If you are a developer, your remote URL must point to our localized GitLab gateway instance.

1.  Configure your remote URL:

git remote set-url origin http://[SERVER_IP]:8929/root/python-api-docker.git

2.  Push exclusively to the production branch using your Personal Access Token:

git push origin production
