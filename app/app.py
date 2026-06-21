import os
import time
import json
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

# -------------------------
# JSON Logger
# -------------------------
def log(event: dict):
    print(json.dumps(event), flush=True)


# -------------------------
# Middleware: Request ID
# -------------------------
@app.before_request
def before_request():
    request.request_id = request.headers.get("X-Request-ID", "unknown")
    request.start_time = time.time()


# -------------------------
# Root Endpoint
# -------------------------
@app.route("/")
def home():
    response = "OK"

    log({
        "request_id": request.request_id,
        "path": "/",
        "method": request.method,
        "status": 200,
        "latency_ms": round((time.time() - request.start_time) * 1000, 2)
    })

    return response


# -------------------------
# Health Endpoint
# -------------------------
@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# -------------------------
# DB Endpoint
# -------------------------
@app.route("/db")
def db():

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )

        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()

        cur.close()
        conn.close()

        log({
            "request_id": request.request_id,
            "path": "/db",
            "method": request.method,
            "status": 200,
            "latency_ms": round((time.time() - request.start_time) * 1000, 2)
        })

        return jsonify({
            "postgres": version[0]
        })

    except Exception as e:

        log({
            "request_id": request.request_id,
            "path": "/db",
            "method": request.method,
            "status": 500,
            "error": str(e),
            "latency_ms": round((time.time() - request.start_time) * 1000, 2)
        })

        return jsonify({"error": str(e)}), 500


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
