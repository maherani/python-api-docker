import time
import uuid
from flask import Flask, request, jsonify, g, Response

from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)

app = Flask(__name__)

# -------------------------
# Prometheus Metrics
# -------------------------

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["endpoint"]
)

# -------------------------
# Middleware
# -------------------------
@app.before_request
def before_request():
    g.request_id = str(uuid.uuid4())
    g.start_time = time.time()


@app.after_request
def after_request(response):

    endpoint = request.path

    # متریک‌های خود Prometheus را دوباره نشمار
    if endpoint != "/metrics":

        latency = time.time() - g.start_time

        REQUEST_COUNT.labels(
            request.method,
            endpoint,
            response.status_code
        ).inc()

        REQUEST_LATENCY.labels(
            endpoint
        ).observe(latency)

    return response
# -------------------------
# Health
# -------------------------
@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "request_id": g.request_id
    })

# -------------------------
# Home
# -------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "API is running",
        "request_id": g.request_id,
        "latency_ms": round((time.time() - g.start_time) * 1000, 2)
    })

# -------------------------
# DB (safe version)
# -------------------------
@app.route("/db")
def db():
    try:
        import psycopg2

        conn = psycopg2.connect(
            host="db",
            database="app",
            user="app",
            password="app"
        )

        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()

        cur.close()
        conn.close()

        return jsonify({
            "db": "ok",
            "result": result,
            "request_id": g.request_id,
            "latency_ms": round((time.time() - g.start_time) * 1000, 2)
        })

    except Exception as e:
        return jsonify({
            "db": "error",
            "error": str(e),
            "request_id": g.request_id
        }), 500

#--------------------------
#   slow  Endpoint
#--------------------------
@app.route("/slow")
def slow():
    time.sleep(3)

    return jsonify({
        "message": "Slow endpoint",
        "request_id": g.request_id
    })

#--------------------------------
# Error Endpoint
#-------------------------------
@app.route("/error")
def error():
    return jsonify({
        "message": "Internal Server Error"
    }), 500


# -------------------------
# Metrics (simple placeholder)
# -------------------------
@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
