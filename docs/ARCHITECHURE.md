# System Architecture Specification

**Project:** python-api-docker
**Architecture Phase:** Production-Grade Containerized Environment (v2.x)
**Focus Areas:** High Availability, Observability, Infrastructure as Code (IaC), and DevSecOps.

---

## 1. High-Level Topology

The system is built on a heavily decoupled, containerized architecture using Docker and orchestrated via Docker Compose. It leverages isolated virtual networks to ensure security, meaning internal services (like the database and backend APIs) are completely shielded from the public internet. External traffic is strictly routed through a reverse proxy.

---

## 2. Core Layers & Components

### 2.1. Ingress & Gateway Layer (Nginx)
* **Role:** Acts as the single entry point (Reverse Proxy) for all client requests.
* **Security:** Implements IP-based rate limiting (10 requests per second) to mitigate DDoS attacks and API abuse.
* **Routing:** Forwards validated HTTP traffic from host port `80` to the internal API container.

### 2.2. Application Layer (Python / Flask)
* **Role:** The core business logic and RESTful API handling.
* **Environment:** Runs on Python 3.11-slim to minimize image size and attack surface.
* **Internal Communication:** Listens on internal port `5000` (not exposed to the host). Connects to the database using Docker's internal DNS (`db:5432`).

### 2.3. Persistence Layer (PostgreSQL)
* **Role:** Relational database management.
* **Version:** PostgreSQL 16.
* **Security:** Operates entirely within the Docker overlay network. Port `5432` is not bound to the host machine, preventing direct external database connections.

### 2.4. Git & CI/CD Infrastructure (Hub-and-Spoke)
* **Local GitLab (Port 8929):** Acts as the localized Git server to ensure development continuity even during external network outages.
* **GitLab Runner:** Bound to the host machine's `/var/run/docker.sock`. It intercepts pushes to the `production` branch, parses `.gitlab-ci.yml`, and orchestrates build/deploy processes dynamically.
* **Repository Mirroring:** Asynchronously syncs the local codebase to the central GitHub repository (Single Source of Truth).

---

## 3. The Observability Stack (O11y)

Monitoring is treated as a first-class citizen, ensuring complete visibility into logs, metrics, and alerts.

1.  **Grafana Alloy (Unified Collector):** Replaces traditional agents (like Promtail). It binds to the Docker socket to dynamically discover containers, collect logs, parse JSON structures, and forward them to Loki.
2.  **Prometheus (Metrics Hub):** Periodically scrapes numeric metrics from:
    * Flask API (`/metrics` via client library).
    * Node Exporter (Host CPU, RAM, Disk).
    * Postgres Exporter (Database performance).
3.  **Grafana Loki (Log Aggregation):** Receives and indexes high-volume, structured logs from Alloy.
4.  **Alertmanager:** Subscribes to Prometheus alert rules (`alerts.yml`). Evaluates states like "High CPU Usage" or "API Down" and dispatches critical alerts to a Telegram Bot via Webhook.
5.  **Grafana (Visualization):** The unified dashboard UI, pre-provisioned to connect seamlessly with both Prometheus and Loki data sources.

---

## 4. Infrastructure as Code (IaC)

Provisioning is strictly automated to eliminate configuration drift:
* **Ansible:** Manages the entire lifecycle of the server setup.
    * `setup-server.yml`: Prepares the host, installs Docker/Git, and configures UFW firewall rules.
    * `deploy-app.yml`: Clones the repository, enforces file permissions (specifically UID 65534 for Prometheus and 10001 for Loki), and spins up the Docker Compose stack.

---

## 5. Network Flow & Port Mapping

To understand how traffic moves through the system, reference this port matrix:

| Service | Internal Port | Host (Exposed) Port | Accessibility |
| :--- | :--- | :--- | :--- |
| **Nginx (Proxy)** | 80 | `80` | Public / Gateway |
| **GitLab (Web/Git)** | 80 / 22 | `8929` / `2222` | Local LAN |
| **Grafana** | 3000 | `3000` | Local LAN (Admin) |
| **Prometheus** | 9090 | `9090` | Local LAN (Admin) |
| **Alertmanager** | 9093 | `9093` | Local LAN (Admin) |
| **Flask API** | 5000 | `None` | Internal Network Only |
| **PostgreSQL** | 5432 | `None` | Internal Network Only |
| **Loki** | 3100 | `None` | Internal Network Only |
| **Grafana Alloy** | 12345 | `None` | Internal Network Only |

---

## 6. Security & DevSecOps Posture

1.  **Least Privilege Execution:** Observability tools (Prometheus, Loki) run as unprivileged non-root users.
2.  **Secret Management:** Database credentials, Telegram bot tokens, and API keys are injected via a `.env` file at runtime and are strictly ignored by `.gitignore`.
3.  **Socket Protection:** The Docker socket is mounted *only* to the GitLab Runner and Grafana Alloy, both of which require it for orchestration and log discovery, respectively.

