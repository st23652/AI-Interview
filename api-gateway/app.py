# api-gateway/app.py
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/interviews', methods=['GET'])
def get_interviews():
    response = requests.get('http://localhost:5001/interviews')
    return jsonify(response.json())

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API Gateway"})

@app.route('/another-route')
def another_route():
    return jsonify({"message": "This is another route"})

@app.route('/interviews/', methods=['GET', 'POST'])
def handle_interviews():
    response = requests.request(request.method, 'http://interview-service:8001' + request.path, json=request.get_json())
    return jsonify(response.json()), response.status_code

@app.route('/jobs/', methods=['GET', 'POST'])
def handle_jobs():
    response = requests.request(request.method, 'http://job-service:8002' + request.path, json=request.get_json())
    return jsonify(response.json()), response.status_code

@app.route('/users/', methods=['GET', 'POST'])
def handle_users():
    response = requests.request(request.method, 'http://user-service:8003' + request.path, json=request.get_json())
    return jsonify(response.json()), response.status_code

@app.route('/ai/', methods=['POST'])
def handle_ai():
    response = requests.request(request.method, 'http://ai-service:8004' + request.path, json=request.get_json())
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
