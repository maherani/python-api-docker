# SRE RUNBOOK — Python API Platform

 1. Service Overview

This system is a production-like Docker-based platform including:

- Flask API
- PostgreSQL Database
- Nginx Reverse Proxy
- Prometheus (metrics)
- Grafana (visualization)

 2. Architecture

Client → Nginx → Flask API → PostgreSQL  
                 ↓  
          Prometheus → Grafana

 3. Start System

```bash
docker-compose up --build -d


4. Verify System
docker-compose ps

Expected:

nginx_proxy → Up
python_api → Up (healthy)
db → Up (healthy)
prometheus → Up
grafana → Up

5. Health Check
curl http://localhost/health

Expected response:

{
  "status": "ok",
  "request_id": "uuid"
}

6. API Endpoints
GET / → Main API
GET /health → Health check
GET /db → Database test
GET /metrics → Prometheus metrics

7. Logs
API logs
docker logs python_api --tail 100
Nginx logs
docker logs nginx_proxy --tail 100
Database logs
docker logs db --tail 100

8. Common Issues
502 Bad Gateway

Cause:

API is down
Nginx cannot reach upstream

Fix:

docker restart nginx_proxy
docker logs nginx_proxy

Check:
proxy_pass must be http://api:5000

API Crash / Restart Loop

Check logs:

docker logs python_api --tail 200

Possible causes:

missing dependency
Python runtime error
missing middleware (request_id / start_time)
Database Connection Issues
docker exec -it db psql -U app -d app

9. Metrics
curl http://localhost/metrics

10. Shutdown System
docker-compose down

11. Full Reset (Clean State)
docker-compose down -v
docker-compose up --build -d

12. Network Architecture

All services communicate via:

app_network (Docker bridge)

Internal routing:

nginx → api:5000
api → db:5432

13. Security Notes
Never commit secrets (tokens, passwords)
Use .gitignore for sensitive files
Database is not exposed externally
nginx is the only public entry point

14. Deployment Flow
Code change
Update documentation
Commit changes
Push to Git
Rebuild system
docker-compose up --build -d

15. Onboarding
git clone <repo>
cd python-api-docker
docker-compose up --build -d

Test:

curl http://localhost/health

16. System Summary

This platform provides:

Stable API service
Database persistence
Reverse proxy routing
Observability stack (metrics + dashboards)

Designed to be:

reproducible
debuggable
production-ready
