#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
'indesx of status'

@app_views.route("/status")
def status():
    'returns a json of status'
    return jsonify({"status": "OK"})
