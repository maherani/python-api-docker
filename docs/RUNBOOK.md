# SRE & Operations Runbook

**Project:** python-api-docker  
**Purpose:** Operational procedures, deployment guides, and incident response playbooks for the engineering team.

---

## 1. Provisioning & Deployment

### 1.1. Environment Variables Setup
Before starting any service, the system requires a `.env` file at the project root. **Never commit this file to Git.**

```ini
# PostgreSQL Secrets
DB_USER=postgres
DB_PASSWORD=SuperSecretPassword
DB_NAME=postgres

# Telegram Alerting Secrets (Alertmanager)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
1.2. Automated Deployment (Ansible)
To provision the host server and deploy the Docker stack from scratch:

Bash
# 1. Setup host (Docker, UFW, Dependencies)
ansible-playbook -i ansible/inventory.ini ansible/setup-server.yml

# 2. Deploy application and configure permissions
ansible-playbook -i ansible/inventory.ini ansible/deploy-app.yml
1.3. Manual Deployment (Docker Compose)
If bypassing Ansible, ensure you run the stack in detached mode:

Bash
docker compose up --build -d
To bring down the infrastructure:

Bash
docker compose down
2. Quick Operations & Status Checks
Check System Status
Bash
# View running containers and ports
docker compose ps

# View real-time aggregated logs for all services
docker compose logs -f

# View logs for a specific service (e.g., the API)
docker compose logs -f app
Restarting Services
If a configuration file (like nginx.conf or prometheus.yml) is updated:

Bash
docker compose restart nginx
# or
docker compose restart prometheus
3. Incident Response Playbooks
🚨 Alert: InstanceDown or API Unreachable
Symptom: Nginx returns 502 Bad Gateway or /health fails.

Diagnosis: 1. Check if the app container is running: docker compose ps app
2. Inspect app logs for Python tracebacks: docker compose logs app

Resolution: Fix code errors and push to Git (CI/CD will redeploy), or rebuild the container manually if testing locally: docker compose up -d --build app.

🚨 Alert: PostgresDown (Database Connection Refused)
Symptom: API returns 500 Internal Server Error on /db or /users endpoints.

Diagnosis:

Check database logs: docker compose logs db

Verify credentials in the .env file match the compose file.

Resolution: Ensure the database volume isn't corrupted. If it's a test environment, you may need to wipe the volume: docker compose down -v and restart.

🚨 Incident: Permission Denied ([error opening dir]) in Prometheus/Loki
Symptom: Prometheus or Loki containers restart repeatedly or throw permission errors in logs.

Cause: These containers run as unprivileged users (UID 65534 for Prometheus, UID 10001 for Loki) for security reasons, but Docker mapped the volumes as root.

Resolution: Run the following commands on the host:

Bash
sudo chown -R 65534:65534 ./prometheus_data
sudo chown -R 10001:10001 ./loki_data
🚨 Incident: Nginx returning 429 Too Many Requests
Symptom: Valid requests are being rejected.

Cause: The Nginx rate limiter is triggered. Current threshold is set to 10 requests per second per IP (rate=10r/s).

Resolution: If this is legitimate traffic, adjust the limit_req_zone parameters in nginx/nginx.conf and reload Nginx:

Bash
docker compose exec nginx nginx -s reload
🚨 Incident: Logs not appearing in Grafana
Symptom: Loki dashboard in Grafana is empty.

Diagnosis:

Check if Grafana Alloy is running and has access to the Docker socket.

View Alloy logs: docker compose logs alloy

Resolution: Ensure /var/run/docker.sock is properly mounted in the alloy container definition inside docker-compose.yml.

4. Observability Service Endpoints
Use these local/LAN endpoints to access operational dashboards:

Service	URL	Purpose
Grafana	http://localhost:3000	Main observability dashboards.
Prometheus	http://localhost:9090	Raw metric querying and target status.
Alertmanager	http://localhost:9093	View active/silenced alerts.
API Health	http://localhost/health	Quick infrastructure validation via Nginx.
Local GitLab	http://localhost:8929	Internal source control and CI/CD pipelines.
