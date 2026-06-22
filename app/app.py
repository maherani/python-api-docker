import time
import uuid
from flask import Flask, request, jsonify, g

app = Flask(__name__)

# -------------------------
# Middleware
# -------------------------
@app.before_request
def before_request():
    g.request_id = str(uuid.uuid4())
    g.start_time = time.time()

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

# -------------------------
# Metrics (simple placeholder)
# -------------------------
@app.route("/metrics")
def metrics():
    return jsonify({
        "status": "metrics-ok"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
