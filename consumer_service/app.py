from flask import Flask, request, jsonify
import time
import logging
import requests
import json
import uuid
import os

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)
app = Flask(__name__)

SERVICE_A = os.getenv("SERVICE_A_URL", "http://127.0.0.1:8080")
TIMEOUT = (float(os.getenv("SERVICE_A_CONNECT_TIMEOUT", "0.5")), float(os.getenv("SERVICE_A_READ_TIMEOUT", "1.0")))
# Separate connect/read timeouts (seconds)
CONNECT_TIMEOUT = float(os.getenv("SERVICE_A_CONNECT_TIMEOUT", "0.5"))
READ_TIMEOUT = float(os.getenv("SERVICE_A_READ_TIMEOUT", "1.0"))
# Retry policy
MAX_RETRIES = int(os.getenv("SERVICE_A_MAX_RETRIES", "2"))

def log_structured(event_type, service, endpoint, status, latency_ms, request_id, error=None, error_type=None, **extra):
    """Log in JSON format for easy parsing."""
    log_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "event": event_type,
        "service": service,
        "endpoint": endpoint,
        "status": status,
        "latency_ms": latency_ms,
        "request_id": request_id
    }
    if error:
        log_data["error"] = error
    if error_type:
        log_data["error_type"] = error_type
    log_data.update(extra)
    if status == "error":
        logger.error(json.dumps(log_data))
    else:
        logger.info(json.dumps(log_data))

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/call-echo")
def call_echo():
    start = time.time()
    request_id = str(uuid.uuid4())[:8]
    msg = request.args.get("msg", "")
    # Simple retry loop with exponential backoff for transient errors
    for attempt in range(0, MAX_RETRIES + 1):
        attempt_start = time.time()
        try:
            r = requests.get(f"{SERVICE_A}/echo", params={"msg": msg}, timeout=TIMEOUT)
            r.raise_for_status()
            data = r.json()
            latency_ms = int((time.time()-start)*1000)
            log_structured("request_complete", "B", "/call-echo", "ok", latency_ms, request_id, msg=msg)
            return jsonify(service_b="ok", service_a=data)
    except requests.exceptions.Timeout as e:
        latency_ms = int((time.time()-start)*1000)
        error_msg = f"Service A timeout after {TIMEOUT}s"
        log_structured("request_failed", "B", "/call-echo", "error", latency_ms, request_id, error=error_msg, error_type="timeout", msg=msg)
        return jsonify(service_b="error", service_a="unavailable", error=error_msg), 504
    except requests.exceptions.ConnectionError as e:
        latency_ms = int((time.time()-start)*1000)
        error_msg = "Service A connection refused"
        log_structured("request_failed", "B", "/call-echo", "error", latency_ms, request_id, error=error_msg, error_type="connection_error", msg=msg)
        return jsonify(service_b="error", service_a="unavailable", error=error_msg), 503
    except Exception as e:
        latency_ms = int((time.time()-start)*1000)
        error_msg = str(e)
        log_structured("request_failed", "B", "/call-echo", "error", latency_ms, request_id, error=error_msg, error_type="unknown", msg=msg)
        return jsonify(service_b="error", service_a="unavailable", error=error_msg), 503

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081)