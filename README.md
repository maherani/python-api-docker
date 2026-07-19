# Production-Grade Containerized Python API Platform

A production-like, fully containerized system engineered for hands-on learning, development, and practice of **DevOps Engineering, Site Reliability Engineering (SRE), and Observability Architectures**. 

This repository simulates real-world backend infrastructure patterns, deliberately structured to emulate industry-standard production problems, system-design constraints, and modern debugging workflows.

---

## 🏛️ System Architecture

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

### Data Persistence Architecture (Host-Mapped Volumes)
To prevent telemetry or state loss during `docker compose down` cycles, long-term state data is isolated to dedicated local directory mounts:
*   `./postgres_data` -> Core transactional database records.
*   `./prometheus_data` -> Long-term Time Series Database (TSDB) metrics data.
*   `./loki_data` -> Chunk indexes and log data storage.
*   `./grafana_data` -> Persistent custom dashboards, plugins, and user configurations.

---

## 🚀 Key Features

*   **Robust Flask Backend Engine:** Built with structured RESTful endpoints including active base routing (`/`), dynamic health statuses (`/health`), structural database connection testing (`/db`), and dedicated telemetry outputs (`/metrics`).
*   **Production-Level Observability Pipeline:** Fully integrated tracing using unique client-side `request_id` context propagation, inline endpoint latency timers, and error-rate calculators.
*   **Persistent Monitoring Stack:** Orchestrated ecosystem utilizing Grafana Alloy for unified metrics collection and runtime log aggregation, feeding Prometheus and Loki data visualization nodes.
*   **Advanced Alerting Mechanics:** Programmatic alerting pipelines evaluating continuous metrics/log thresholds via Alertmanager with dedicated automated targets like an active Telegram Bot channel.
*   **Isolated Database Architecture:** PostgreSQL runs fully enclosed within private internal overlay networks, secured with health checks to prevent dependent backend services from spawning prematurely.
*   **Decoupled Reverse Proxy Layer:** Standalone Nginx layer providing strict path-routing separation, configured cleanly inside isolated configuration structures (`conf.d/default.conf`).

---

## 🛠️ Technology Stack
*   **Core Backend Framework:** Python (Flask Engine)
*   **Data Tier Layer:** PostgreSQL 16
*   **Gateway / Load Balancer:** Nginx (Alpine Base)
*   **Orchestration Engine:** Docker & Docker Compose v2
*   **Observability Matrix:** Prometheus, Grafana Loki, Grafana Alloy, Alertmanager

---

## 📋 Prerequisites & Configuration Management

### Environment File Setup (`.env`)
Before instantiating the cluster, a root-level `.env` file must be provisioned. This file holds local cluster properties and secure credentials. **Never commit this file or raw secrets to source control.**

Create a file named `.env` in the repository root directory:
```env
# ==============================================================================
# DATABASE SERVICE CONFIGURATION
# ==============================================================================
DB_USER=myuser
DB_PASSWORD=mypassword
DB_NAME=mydb
DB_HOST=db

# ==============================================================================
# ALERTS & NOTIFICATIONS OVERLAY (ALERTMANAGER TARGETS)
# ==============================================================================
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

---

## ⚡ Quick Start

### 1. Project Initialization & Provisioning
Clone the repository and prepare the required local persistence directories on the host operating system:
```bash
# Clone the repository endpoint
git clone https://github.com/your-username/python-api-docker.git
cd python-api-docker

# Bootstrap persistent local directory volumes
mkdir -p prometheus_data loki_data grafana_data postgres_data

# Grant standard access permissions for Docker engine execution loops
sudo chmod -R 777 prometheus_data loki_data grafana_data postgres_data
```

### 2. Launching the Infrastructure
Compile application modifications and spin up the complete container architecture detached in the background:
```bash
docker compose up --build -d
```

### 3. Verify System Runtime Status
Validate that the entire ecosystem is healthy and operational:
```bash
docker compose ps
```
**Expected Deterministic Runtime Mapping:**
*   `nginx_proxy` -> **Up (Active / Listening)**
*   `python_api` -> **Up (Healthy)**
*   `db` -> **Up (Healthy)**
*   `prometheus` -> **Up (Active)**
*   `loki` -> **Up (Active)**
*   `grafana` -> **Up (Active)**

### 4. Interactive Endpoints Verification
Test edge gateway functionality using request requests:
```bash
curl http://localhost/
curl http://localhost/health
curl http://localhost/db
curl http://localhost/metrics
```

---

## 📊 Core Observability Targets & Management Dashboards

Once all system workflows take an **Up** status, the internal administrative consoles can be reached directly via web interfaces:

*   **Prometheus Target Matrix Console:** Available natively at `http://localhost:9090` (Verify targets inside the Status -> Targets dashboard).
*   **Grafana Custom Visual Platform:** Running natively at `http://localhost:3000`. Initial metrics dashboards are structured out-of-the-box (manually configure Loki and Prometheus references upon first launch if required).

---

## 🔍 Verification & Telemetry Query Handbook

To query and inspect the pipeline data inside the **Grafana Explore** panel (`http://localhost:3000/explore`), use the following standard industry configurations:

### 1. Log Analytics (Loki Engine)
To parse, filter, and analyze the structured JSON telemetry records generated by the application, select the **Loki** data source and execute this query:
```logql
{container="/api"}
 
### 2. Performance Latency Analytics (Prometheus Mode)
To calculate and graph the exact application response times (Latency) by endpoint without the parsing overhead of log structures, switch the data source to **Prometheus** and inject this formula:
```promql
sum(rate(http_request_duration_seconds_sum{job="api"}[1m])) by (endpoint) 
/ 
sum(rate(http_request_duration_seconds_count{job="api"}[1m])) by (endpoint)

---

## 📐 Production Simulation Design Rules

*   **Keep Things Simple:** Keep infrastructure decoupled. Avoid unnecessary system complications; isolate components early.
*   **Telemetry Mandatory:** Systems are built to fail; observability is integrated directly into application workflows rather than injected as a secondary consideration.
*   **Incremental Refactoring:** Code components are altered through controlled updates. Complete script rewrites are forbidden to mimic realistic system lifecycles.
*   **Zero-Trust Secrets Handling:** Keep configurations externalized. Sensitive variables must remain strictly outside configuration code blocks.

---

## ⚠️ Known Issues & Architectural Constraints
*   `GET /db` can occasionally drop or manifest connection fluctuations during database provisioning phases.
*   Middleware components are sensitive to execution hierarchies within Flask execution trees.
*   Grafana analytics layers require manual setup steps if default volume maps do not persist locally.

---

## 🔮 Future Architecture Roadmap
*   Full integration of automated, production-grade alert routing models using Alertmanager configurations.
*   Deeper code integration with OpenTelemetry components to facilitate true end-to-end tracing.
*   Advanced CI/CD deployment routines written explicitly inside GitHub Actions.
*   Porting current cluster topologies to bare-metal Kubernetes objects.
*   Enabling dynamic service auto-scaling patterns via replica strategies inside Docker Compose.

---

## 📝 Lessons Learned Documentation
1.  **Middleware Execution Order:** The sequential loading sequence of middleware layers is highly critical inside Flask runtime instances.
2.  **Reverse Proxy Reliability:** Minor structural errors inside proxy routing maps (`nginx.conf`) can lead to complete service outages at the gateway.
3.  **Observability Integration:** Telemetry hooks must be explicitly designed during initial service design stages rather than introduced later.

---

## 🛠️ Comprehensive Troubleshooting & Multi-Environment Configuration

When establishing this platform inside restrictive corporate local networks, distinct operating systems, or secondary machines, unexpected networking and disk permission bottlenecks can occur. Below is the automated remediation matrix:

### 1. Docker Host Hub Restrictions & Container Timeout Resolutions
**Problem:** In isolated or highly restricted enterprise networks, image retrieval cycles fail with network timeouts or metadata acquisition faults (`load metadata...`).

**Remediation:** Configure a verified local mirror registry layer inside the core daemon configuration.
1. Access **Docker Desktop Settings** -> **Docker Engine**.
2. Update the JSON properties object to append the local registry fallback mirror configuration:
```json
{
  "registry-mirrors": [
    "https://docker-mirror.liara.ir"
  ]
}
```
3. Choose **Apply & Restart**. Verify pull status via standard terminal checks:
```bash
docker pull postgres:16
docker pull nginx:alpine
docker pull prom/prometheus:latest
```

### 2. WSL2 Linux Subsystem Dynamic Network Interruptions (Windows 11 Platform)
**Problem:** The local instance loses general ping access parameters (`ping google.com` fails), disrupting connectivity workflows to Docker Hub endpoints.

**Remediation:** Force the Windows subsystem to map its virtual network configurations to the host interface directly.
1. Open PowerShell and completely isolate the Linux execution system:
   ```powershell
   wsl --shutdown
   ```
2. Open the primary User Directory path (`Win + R` -> `%userprofile%`).
3. Generate or append modifications to a file named `.wslconfig` adding these instructions:
   ```ini
   [wsl2]
   networkingMode=mirrored
   dnsTunneling=true
   ```
4. Restart your terminal emulator instance to cleanly bind the updated adapter context.

### 3. Metric/Log Engine Write Faults (`Permission Denied`)
**Problem:** Prometheus or Loki engines enter cyclical crash loops (`Restarting` or `Exit 1` statuses) or report specific filesystem permissions bottlenecks inside runtime tracking output files:
```text
prometheus  | err="open /prometheus/queries.active: permission denied"
loki        | err="mkdir /loki/rules: permission denied"
```

**Remediation:** Prometheus and Loki execute under unprivileged security profiles (UIDs `65534` and `10001` respectively) to emulate secure production systems. Fix host-level storage volume mappings by modifying ownership IDs to correspond with internal service users:
```bash
# Completely drop active runtime components
docker compose down

# Fix Prometheus (UID 65534)
sudo chown -R 65534:65534 prometheus_data
sudo chmod -R 775 prometheus_data

# Fix Loki (UID 10001)
sudo chown -R 10001:10001 loki_data
sudo chmod -R 777 loki_data

# Re-instantiate the environment clean
docker compose up -d
```
## 🚀 Git Workflow & Deployment Process

To ensure server security and maintain a clear separation of roles, container deployment is configured as a two-stage (approval-based) workflow. Developers are not permitted to deploy directly to the production server.

### 1. Developer Workflow (Development & Testing)
Developers must push their verified changes to the `main` branch or submit a Pull Request:

```bash
git checkout main
git pull origin main
# Make your changes...
git add .
git commit -m "fix: description of changes"
git push origin main

Result: This action triggers only the linting, security scanning, and testing jobs (test-and-build) in GitHub Actions. The server deployment job (deploy) is automatically Skipped, keeping the server untouched.
2. DevOps Admin Workflow (Final Review & Deployment)
New code updates apply to the production containers only when the DevOps Admin reviews the code and syncs it with the production branch. Pushing to this branch serves as the official Manual Approval:
# Switch to the dedicated deployment branch
git checkout production

# Merge the approved changes from the main branch
git merge main

# Push to trigger the live server deployment
git push origin production

Result: The production branch workflow initializes. Once the test suite passes successfully, the local runner builds the Docker images and updates the live container stack.
