from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
