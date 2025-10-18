#!/usr/bin/python3.13

#FlaskAPI - Backend Application

from flask import Flask, request, jsonify
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time , sys, logging,json

app = Flask(__name__)

# Metric to instrument total request counter
REQUEST_COUNT = Counter(
    "flaskapi_request_count",
    "Total number of requests by method and endpoint",
    ["service","method", "endpoint", "http_status"]
)

# Metric to instrument total request latency 
REQUEST_LATENCY = Histogram(
    "flaskapi_request_latency_seconds",
    "Request latency in seconds",
    ["service","method", "endpoint"]
)

# Metric to instrument total request error counter 
REQUEST_ERROR_COUNT = Counter(
    "flaskapi_error_count",
    "Total number of error responses (HTTP 4xx/5xx)",
    ["service","method", "endpoint", "http_status"]
)

# Metric to catch unhandled exception by application
EXCEPTION_COUNT = Counter(
    "flaskapi_exception_count",
    "Total number of uncaught exceptions in the Flask app",
    ["exception_type"]
)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "level": record.levelname,
            "service":"flaskapi-backend",
            "message": record.getMessage(),
            "logger": record.name,
            "time": self.formatTime(record, self.datefmt),
        }
        return json.dumps(log_data)

# Disable default logging
logging.getLogger('werkzeug').disabled = True
app.logger.propagate = False 
app.logger.disabled = True  

# Enable custom logging - jsonformat
custom_logger = logging.getLogger("flaskapi")
custom_logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())


custom_logger.addHandler(handler)
custom_logger.propagate = False



@app.before_request
def start_timer():
    request.start_time = time.time()


@app.after_request
def record_metrics(response):
    # Stop the latency timer
    latency = time.time() - request.start_time

    # Record Latency metric - duration
    REQUEST_LATENCY.labels("flaskapi-backend",request.method, request.path).observe(latency)

    # Record request metric - counter
    REQUEST_COUNT.labels("flaskapi-backend",request.method, request.path, response.status_code).inc()

    custom_logger.info(
        f"{request.method} {request.path} {response.status_code} {latency:.4f}s"
    )

    # Record error metric for 4xx/5xx
    if 400 <= response.status_code < 600:
        REQUEST_ERROR_COUNT.labels("flaskapi-backend",request.method, request.path, response.status_code).inc()

    return response

@app.route('/')
def home():
    return jsonify(message="Hello, World!")

@app.route('/api')
def apistatus(response):
    current_timestamp = datetime.now()
    return jsonify({
        "status": "ok",
        "date": current_timestamp.isoformat(),
        "status_code" : response.status_code,
        "path" : request.path,
        "method" : request.method
    })

@app.route('/health')
def healthstatus(response):
    current_timestamp = datetime.now()
    return jsonify({
        "status": "ok" ,
        "date": current_timestamp.isoformat(),
        "status_code" : response.status_code
    })

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


@app.errorhandler(Exception)
def handle_exception(e):
    """Catch unhandled exceptions and count them."""
    EXCEPTION_COUNT.labels(type(e).__name__).inc()
    response = jsonify({"error": str(e)})
    response.status_code = 500
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=False)

