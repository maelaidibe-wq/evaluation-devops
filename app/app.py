from flask import Flask, jsonify, request
import redis
import os
import time

from prometheus_client import Counter, Histogram, Gauge
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)

request_count = Counter(
    "http_requests_total",
    "Nombre total de requetes HTTP",
    ["endpoint", "code"]
)

request_duration = Histogram(
    "http_request_duration_seconds",
    "Duree des requetes HTTP",
    ["endpoint"]
)

app_version = Gauge(
    "app_version_info",
    "Version de l'application",
    ["version"]
)

app_version.labels(
    version=os.getenv("COMMIT_SHA", "dev")
).set(1)


@app.before_request
def start_timer():
    request.start_time = time.time()


@app.after_request
def save_metrics(response):
    duration = time.time() - request.start_time

    request_count.labels(
        endpoint=request.path,
        code=response.status_code
    ).inc()

    request_duration.labels(
        endpoint=request.path
    ).observe(duration)

    return response


@app.route("/")
def home():
    return jsonify(message="Evaluation DevOps")


@app.route("/health")
def health():
    try:
        redis_client.ping()
        return jsonify(status="ok"), 200
    except redis.RedisError:
        return jsonify(status="error"), 500


@app.route("/visits")
def visits():
    count = redis_client.incr("visits")
    return jsonify(visits=count)


@app.route("/simulate-error")
def simulate_error():
    return jsonify(error="Erreur de test"), 500


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
