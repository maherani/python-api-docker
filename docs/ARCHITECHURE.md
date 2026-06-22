# Architecture Documentation

## Request Flow

1. Client sends request
2. Request reaches Nginx
3. Nginx forwards request to Flask API
4. Flask processes request
5. Optional database access
6. Response returned to Nginx
7. Response returned to client

---

## Logging Flow

Before request:

* Request ID generated or extracted
* Start time stored

After request:

* Latency calculated
* Structured log generated

Example:

{
"request_id": "abc123",
"path": "/db",
"method": "GET",
"status": 200,
"latency_ms": 15.5
}

---

## Container Topology

nginx_proxy
|
+--> python_api
|
+--> postgres

---

## Network Model

Only Nginx is exposed externally.

Port 80 -> Nginx

Flask API remains internal.

PostgreSQL remains internal.

This design reduces attack surface and follows production best practices.
