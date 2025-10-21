#!/usr/bin/python3.13

from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Hello, World!")

@app.route('/api')
def apistatus():
    current_timestamp = datetime.now()
    return jsonify({
        "status": "ok",
        "date": current_timestamp.isoformat()  
    })

@app.route('/health')
def healthstatus():
    current_timestamp = datetime.now()
    return jsonify({
        "status": "ok"  
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)