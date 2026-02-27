from flask import Flask
from flask_cors import CORS
import mysql.connector
import time

app = Flask(__name__)
CORS(app) # Required for the UI on 9090 to talk to Backend on 5005

@app.route('/api/welcome/<service_name>')
def welcome(service_name):
    # This proves the Backend is working
    return f"Welcome to the {service_name} Service!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
