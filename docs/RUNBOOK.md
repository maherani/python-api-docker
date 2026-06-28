SRE RUNBOOK — python-api-docker

Version: 2026-06-28
Scope: Operational procedures for runtime, debugging, and incident recovery

1. Purpose

This runbook defines operational procedures for:

Running the system
Debugging issues
Recovering from failures
Handling incidents

Target audience:

Developers
DevOps engineers
SRE engineers
2. Start System
docker-compose up --build -d
3. Verify System Health
docker-compose ps
Expected State
nginx_proxy → Up
python_api → Up (healthy)
db → Up (healthy)
prometheus → Up
grafana → Up
4. Stop System
docker-compose down
5. Full Reset (Clean State)

⚠️ Danger: removes volumes and data

docker-compose down -v
docker-compose up --build -d
6. Logs
6.1 API Logs
docker logs python_api --tail 100
6.2 Nginx Logs
docker logs nginx_proxy --tail 100
6.3 Database Logs
docker logs python-api-docker_db_1 --tail 100
7. Health Checks
7.1 API Health
curl http://localhost/health

Expected:

{
  "status": "ok"
}
7.2 Database Check
curl http://localhost/db

If failing:

Check DB container
Check API logs
Verify network connectivity
7.3 Metrics Check
curl http://localhost/metrics
8. Common Issues
8.1 502 Bad Gateway (Nginx)
Symptoms
Nginx returns 502
Causes
API is down
Incorrect upstream configuration
Fix
docker restart nginx_proxy
docker logs nginx_proxy

Ensure upstream points to:

python_api:5000
8.2 API Crash Loop
Symptoms
python_api restarting continuously
Debug
docker logs python_api --tail 200
Common Causes
Missing Python dependencies
Middleware failure (request_id / timing)
Database connection failure
8.3 Database Connection Error
Debug
docker exec -it python-api-docker_db_1 psql -U postgres
8.4 Prometheus Not Scraping

Check:

http://localhost:9090/targets
9. Incident Severity Model
SEV1 (Critical)
API down
Database unreachable
Full system failure

Action:

Immediate restart
Check logs
SEV2 (High)
Partial endpoint failure
Metrics broken
SEV3 (Low)
Logging issues
Dashboard missing data
10. Debug Workflow

When system breaks:

1. docker-compose ps
2. docker logs <service>
3. check network
4. restart service
11. Observability Tools
Prometheus → metrics collection
Grafana → dashboards
Flask /metrics → exporter endpoint
12. Known Stable State

System is healthy when:

nginx_proxy → Up
python_api → Up (healthy)
db → Up (healthy)
prometheus → Up
grafana → Up
13. Golden Rule

Never apply changes without:

checking logs
verifying container health
updating PROJECT_STATE.md
