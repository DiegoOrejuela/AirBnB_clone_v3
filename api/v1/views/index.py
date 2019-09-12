#!/usr/bin/python3
'index of status'
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    'returns a json of status'
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """retrieves the number of each objects by type"""
    dict_classes = {"amenities": "Amenity", "cities": "City",
                    "places": "Place", "reviews": "Review",
                    "states": "State", "users": "User"}
    new_dict = {}
    for key, value in dict_classes.items():
        new_dict[key] = storage.count(value)
    return jsonify(new_dict)
