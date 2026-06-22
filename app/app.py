import time
import uuid
import json
import logging   # 👈 ADD THIS LINE
import psycopg2
from flask  import g
from flask import Flask, request, jsonify

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

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
def start_request():
    g.start_time = time.time()
    g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

@app.after_request
def log_request(response):
    latency = round((time.time() - g.start_time) * 1000, 2)

    log_data = {
        "request_id": g.request_id,
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "latency_ms": latency
    }

    print(json.dumps(log_data))

    return response

# -------------------------
# Root Endpoint
# -------------------------
@app.route("/")
def home():
    response = "OK"

    log({
	"request_id": g.request_id,
        "path": "/",
        "method": request.method,
        "status": 200,
        "latency_ms": round((time.time() - g.start_time) * 1000, 2)
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
            "request_id": g.request_id,
            "path": "/db",
            "method": request.method,
            "status": 200,
            "latency_ms": round((time.time() - g.start_time) * 1000, 2)
        })

        return jsonify({
            "postgres": version[0]
        })

    except Exception as e:

        log({
            "request_id": g.request_id,
            "path": "/db",
            "method": request.method,
            "status": 500,
            "error": str(e),
            "latency_ms": round((time.time() - g.start_time) * 1000, 2)
        })

        return jsonify({"error": str(e)}), 500


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
