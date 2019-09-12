#!/usr/bin/python3
"""api file with the api flask instance"""
from flask import Flask, render_template, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def shutdown_session(exception=None):
    "close the session"
    storage.close()


@app.errorhandler(404)
def not_found(e):
    'error handling'
    return jsonify({"error": "Not found"})

if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST"),
            port=int(getenv("HBNB_API_PORT")), threaded=True)
