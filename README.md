# Python API Docker Demo

## Overview

This project is a sample production-style API stack built with:

* Flask
* PostgreSQL
* Docker
* Docker Compose
* Nginx Reverse Proxy

The project demonstrates:

* Containerized application deployment
* Reverse proxy configuration
* Health checks
* Database connectivity
* Structured logging
* Request tracing using Request ID

---

## Architecture

Client
↓
Nginx (Port 80)
↓
Flask API (Port 5000)
↓
PostgreSQL (Port 5432)

---

## Components

### Nginx

Responsibilities:

* Reverse proxy
* Request forwarding
* Header forwarding
* Public entry point

### Flask API

Responsibilities:

* Business logic
* Health endpoint
* Database endpoint
* Structured logging

### PostgreSQL

Responsibilities:

* Persistent data storage
* Application database

---

## Endpoints

### Health Check

GET /health

Response:

{
"status": "ok"
}

### Database Check

GET /db

Response:

{
"status": "ok"
}

### Root Endpoint

GET /

Response:

{
"message": "hello"
}

---

## Logging

Each request generates a structured log entry.

Example:

{
"request_id": "test-1",
"path": "/",
"method": "GET",
"status": 200,
"latency_ms": 0.03
}

---

## Local Development

Build:

docker-compose build

Start:

docker-compose up -d

Stop:

docker-compose down

Logs:

docker logs python_api

---

## Git Workflow

Pull latest changes:

git pull origin main

Push changes:

git add .
git commit -m "description"
git push origin main

---

## Environment Variables

Configured through .env file.

Database settings:

POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD

---

## Project Goal

The purpose of this repository is learning:

* Docker
* Flask
* PostgreSQL
* Nginx
* Observability
* Production-style deployment
