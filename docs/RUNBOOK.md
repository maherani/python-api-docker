# Operations Runbook

## Verify Containers

docker-compose ps

Expected:

* nginx_proxy -> Up
* python_api -> Up (healthy)
* postgres -> Up (healthy)

---

## Check Logs

Application:

docker logs python_api --tail 100

Nginx:

docker logs nginx_proxy --tail 100

Database:

docker logs python-api-docker_db_1 --tail 100

---

## Test Endpoints

Health:

curl http://localhost/health

Database:

curl http://localhost/db

---

## Common Problems

### 500 Internal Server Error

Check:

docker logs python_api

Common causes:

* Python exception
* Missing imports
* Database connection failure

---

### Nginx 502 Bad Gateway

Check:

docker ps

Verify:

* python_api is running
* nginx.conf upstream name is correct

---

### Database Connection Failure

Verify:

* PostgreSQL container is healthy
* Environment variables are correct

---

### Container Restart Loop

Check:

docker logs python_api

Most restart loops are caused by application startup errors.

---

## Recovery Procedure

1. Pull latest code
2. Rebuild containers

docker-compose down
docker-compose up --build -d

3. Verify health

docker-compose ps

4. Test endpoints

curl http://localhost/health
curl http://localhost/db
