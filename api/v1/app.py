#!/usr/bin/python3
"""
Starts Flask web application
"""
from models import storage
from api.v1.views import app_views
from flask import Blueprint
from flask import Flask
import os
import threading


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(self):
    storage.close()


if __name__ == "__main__":
    host_ip = os.getenv('HBNB_API_HOST', '0.0.0.0')
    host_port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host_ip, port=host_port, threaded=True)
