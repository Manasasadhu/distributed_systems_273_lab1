from flask import Flask, request, jsonify
import time
import logging
import json
import uuid

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)
app = Flask(__name__)

def log_structured(event_type, service, endpoint, status, latency_ms, request_id, error=None, **extra):
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
    log_data.update(extra)
    logger.info(json.dumps(log_data))

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/echo")
def echo():
    start = time.time()
    request_id = str(uuid.uuid4())[:8]
    msg = request.args.get("msg", "")
    resp = {"echo": msg}
    latency_ms = int((time.time()-start)*1000)
    log_structured("request_complete", "A", "/echo", "ok", latency_ms, request_id, msg=msg)
    return jsonify(resp)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)