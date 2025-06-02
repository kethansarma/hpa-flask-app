# Initialize using environment variables
import sqlite3
import redis
import os
from elasticapm.contrib.flask import ElasticAPM
from flask import Flask, jsonify, request
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from dotenv import load_dotenv
from datetime import datetime
import logging, random
# logging.basicConfig(filename='app.log', level=logging.INFO)
# print(logging.getLoggerClass().root.handlers[0].baseFilename)
load_dotenv()


app = Flask(__name__)
apm = ElasticAPM(app)
redis_conn = redis.Redis(host="localhost", port=6379, db=0)
gauge = Gauge('custom_metric', 'Custom Metric Description')


@app.route('/set-data', methods=['POST'])
def set_data():
    prediction_value = request.form["prediction"]
    redis_conn.set('prediction', str(prediction_value))
    return jsonify({"status": "success", "message": "Data set in Redis"})

@app.route('/get-data')
def get_data():
    value = redis_conn.get('prediction')
    return jsonify({"status": "success", "value": value.decode('utf-8') if value else None})

@app.route('/')
def index():
    app.logger.warning(f"Warning Index route")
    return '<h1>Hello, World!</h1>'
@app.route('/logs', methods=["GET"])
def getLogs():
    app.logger.warning(f"Warning log route info logs route")
    return '<h1>Hello, World! Logs</h1>'
@app.route("/log", methods=["GET"])
def log():
    # Get the current date and time
    now = datetime.now()

# Format the datetime object into a readable string
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    message = f'Log {current_time}' #request.form["message"]
    app.logger.warning(f"Warning log route info {current_time}")
   

    # Store the message in SQLite
    sqlite_conn = sqlite3.connect("logs.db")
    cursor = sqlite_conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS logs (message text)")
    cursor.execute("INSERT INTO logs (message) values (?)", (message,))
    sqlite_conn.commit()
    sqlite_conn.close()

    # Store the message in Redis
    redis_conn.rpush("logs", message)

    return "Logged: {}".format(message)
@app.route('/metrics')
def metrics():
    value = redis_conn.get('prediction')
    gauge.set(int(value))
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
@app.route('/take', methods=['GET'])
def getTake():
    return '<h1>Hello, World! Take</h1>'
if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")