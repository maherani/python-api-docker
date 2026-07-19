import time
import uuid
import json
import logging
import sys
from flask import Flask, request, jsonify, g, Response

from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)

app = Flask(__name__)

# ==============================================================================
# STRUCTURED JSON LOGGING SETUP
# ==============================================================================
# Configure base logging to standard output for container telemetries
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("python-api")

# Disable default Flask/Werkzeug text logs to eliminate noisy /metrics traffic
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

def log_json(level, message, extra=None):
    """Helper function to output single-line JSON log vectors for Loki parsing."""
    log_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": level,
        "message": message,
        "request_id": getattr(g, 'request_id', 'N/A'),
    }
    if extra:
        log_data.update(extra)
    print(json.dumps(log_data), flush=True)

# ==============================================================================
# PROMETHEUS TELEMETRY METRICS
# ==============================================================================
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

# ==============================================================================
# INTERACTIVE MIDDLEWARE LAYERS
# ==============================================================================
@app.before_request
def before_request():
    """Instantiates runtime context trackers for tracing validation chains."""
    g.request_id = str(uuid.uuid4())
    g.start_time = time.time()

@app.after_request
def after_request(response):
    """Evaluates downstream responses, commits counters, and serializes logs."""
    endpoint = request.path
    latency = 0.0  # Initialize latency to prevent UnboundLocalError

    # Filter internal health metric endpoints to preserve bandwidth stability
    if endpoint != "/metrics":
        start_time = getattr(g, 'start_time', None)
        if start_time:
            latency = time.time() - start_time

        # Export numerical vectors to Prometheus scrape loop
        REQUEST_COUNT.labels(
            request.method,
            endpoint,
            response.status_code
        ).inc()

        REQUEST_LATENCY.labels(
            endpoint
        ).observe(latency)

        # Ship single-line structural JSON block to stdout stream
        log_json(
            level="INFO" if response.status_code < 400 else "ERROR",
            message=f"Request processed: {request.method} {endpoint}",
            extra={
                "method": request.method,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "latency_ms": round(latency * 1000, 2),
                "ip": request.remote_addr
            }
        )

    return response

# ==============================================================================
# CORE ROUTING APPLICATION ENDPOINTS
# ==============================================================================
@app.route("/")
def home():
    """Root confirmation status check endpoint."""
    start_time = getattr(g, 'start_time', time.time())
    return jsonify({
        "message": "API is running",
        "request_id": getattr(g, 'request_id', 'N/A'),
        "latency_ms": round((time.time() - start_time) * 1000, 2)
    })

@app.route("/health")
def health():
    """Basic infrastructure validation layer."""
    return jsonify({
        "status": "ok",
        "request_id": getattr(g, 'request_id', 'N/A')
    })

@app.route("/db")
def db():
    """Evaluates structural upstream persistent channel metrics."""
    start_time = getattr(g, 'start_time', time.time())
    try:
        # Isolated import to prevent container initialization crashes
        import psycopg2

        # Connect utilizing internal overlay network bridges
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

        log_json("INFO", "Database query executed successfully")
        return jsonify({
            "db": "ok",
            "result": result,
            "request_id": getattr(g, 'request_id', 'N/A'),
            "latency_ms": round((time.time() - start_time) * 1000, 2)
        })

    except Exception as e:
        log_json("CRITICAL", f"Database connection failed: {str(e)}")
        return jsonify({
            "db": "error",
            "error": str(e),
            "request_id": getattr(g, 'request_id', 'N/A')
        }), 500

@app.route("/slow")
def slow():
    """Simulates downstream resource starvation timelines."""
    time.sleep(3)
    return jsonify({
        "message": "Slow endpoint",
        "request_id": getattr(g, 'request_id', 'N/A')
    })

@app.route("/error")
def error():
    """Simulates standard server validation exception instances."""
    log_json("ERROR", "Simulated internal server error endpoint triggered")
    return jsonify({
        "message": "Internal Server Error",
        "request_id": getattr(g, 'request_id', 'N/A')
    }), 500

@app.route("/metrics")
def metrics():
    """Exposes current numerical telemetry records to Prometheus."""
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # nosec B104
