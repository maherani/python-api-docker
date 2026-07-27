import os
import json
import logging
import sys
import time
import uuid

from flask import Flask, Response, g, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)


# Fetch environment variables to construct the database connection string
db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'postgres')
db_name = os.environ.get('DB_NAME', 'postgres')
db_host = os.environ.get('DB_HOST', 'db')

# Configure SQLAlchemy database settings
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask extensions
db_ext = SQLAlchemy(app)
migrate = Migrate(app, db_ext)

# ==============================================================================
# DATABASE MODELS
# ==============================================================================
class User(db_ext.Model):
    __tablename__ = 'users'

    id = db_ext.Column(db_ext.Integer, primary_key=True)
    username = db_ext.Column(db_ext.String(80), unique=True, nullable=False)
    email = db_ext.Column(db_ext.String(120), unique=True, nullable=False)
    created_at = db_ext.Column(db_ext.DateTime, server_default=db_ext.func.now())

    def to_dict(self):
        """Helper method to serialize the user object into a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

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
@app.route("/users", methods=["POST"])
def create_user():
    """Creates a new user record in the database from a JSON payload."""
    data = request.get_json()

    # Validate incoming payload
    if not data or not data.get("username") or not data.get("email"):
        log_json("WARNING", "Invalid payload for user creation")
        return jsonify({
            "error": "Missing 'username' or 'email' in request body",
            "request_id": getattr(g, 'request_id', 'N/A')
        }), 400

    try:
        # Instantiate and populate the new User model
        new_user = User(
            username=data["username"],
            email=data["email"]
        )

        # Commit the transaction to the database
        db_ext.session.add(new_user)
        db_ext.session.commit()

        log_json("INFO", f"User created successfully: {new_user.username}")
        return jsonify({
            "message": "User created successfully",
            "user": new_user.to_dict(),
            "request_id": getattr(g, 'request_id', 'N/A')
        }), 201

    except SQLAlchemyError as e:
        # Rollback the session in case of duplicate entries or integrity errors
        db_ext.session.rollback()
        log_json("ERROR", f"Database transaction failed: {e!s}")
        return jsonify({
            "error": "Database error (e.g., username or email already exists)",
            "request_id": getattr(g, 'request_id', 'N/A')
        }), 500


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
            host=os.environ.get('DB_HOST', 'db'),
            database=os.environ.get('DB_NAME', 'postgres'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', 'postgres')
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

    except Exception as e: # noqa: BLE001
        log_json("CRITICAL", f"Database connection failed: {e!s}")
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
# Listen on all network interfaces (0.0.0.0) for container networking
    app.run(host="0.0.0.0", port=5000)  # nosec B104
