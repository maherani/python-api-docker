# SRE RUNBOOK — Python API Docker Platform

## Purpose

This document defines operational procedures for running, debugging, and recovering the system.

It is intended for:

- Developers
- DevOps engineers
- SRE engineers

---

# 1. Start System

```bash id="start_cmd"
docker-compose up --build -d
2. Verify System Health
docker-compose ps

Expected:

nginx_proxy → Up
python_api → Up (healthy)
db → Up (healthy)
prometheus → Up
grafana → Up
3. Stop System
docker-compose down
4. Full Reset (Clean State)

⚠️ Use carefully

docker-compose down -v
docker-compose up --build -d
5. View Logs
API Logs
docker logs python_api --tail 100
Nginx Logs
docker logs nginx_proxy --tail 100
Database Logs
docker logs python-api-docker_db_1 --tail 100
6. Health Checks
API Health
curl http://localhost/health

Expected:

{
  "status": "ok"
}
Database Check
curl http://localhost/db

If failing:

Check postgres container
Check API logs
Metrics Check
curl http://localhost/metrics
7. Common Issues
7.1 502 Bad Gateway (Nginx)

Symptoms:

nginx returns 502

Causes:

API down
wrong upstream config

Fix:

docker restart nginx_proxy
docker logs nginx_proxy

Check config:

must route to python_api:5000
7.2 API Crash Loop

Symptoms:

python_api restarting

Check logs:

docker logs python_api --tail 200

Common causes:

missing Python dependency
missing middleware (request_id, start_time)
DB connection failure
7.3 Database Connection Error

Check:

docker exec -it python-api-docker_db_1 psql -U postgres
7.4 Prometheus Not Scraping

Check targets:

http://localhost:9090/targets
8. Incident Response Model
Severity Levels
SEV1 (Critical)
API down
DB unreachable
full system failure

Action:

restart system
check logs immediately
SEV2 (High)
partial endpoint failure
metrics broken
SEV3 (Low)
logging issues
dashboard missing data
9. Debug Workflow

If system breaks:

Check containers
docker-compose ps
Check logs
docker logs <service>
Check network
docker network ls
Restart service
docker restart <service>
10. Observability Tools
Prometheus → metrics
Grafana → dashboards
Flask /metrics endpoint
11. Known Stable State

System is healthy when:

nginx → Up
api → Up (healthy)
db → Up (healthy)
prometheus → Up
grafana → Up
12. Golden Rule

Never apply large changes without:

checking logs
verifying container health
updating PROJECT_STATE.md
