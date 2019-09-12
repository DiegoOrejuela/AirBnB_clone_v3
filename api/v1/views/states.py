#!/usr/bin/python3
'states handling for api'
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state_by_id(state_id):
    'retrive an object into a json'
    if not request.get_json():
        abort(400, "Not a JSON")

    state = storage.get("State", state_id)

    if state:
        for key, value in request.get_json().items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(state, key, value)
        state.save()
    else:
        abort(404)

    return jsonify(state.to_dict()), 200


@app_views.route('/states', methods=['POST'])
def post_state_by_id():
    'retrive an object into a json'
    if not request.get_json():
        abort(400, "Not a JSON")
    if not request.get_json().get("name"):
        abort(400, "Missing name")

    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states")
def states():
    """retrive an object into a json"""
    list_states = []
    for key, value in storage.all("State").items():
        list_states.append(value.to_dict())
    return jsonify(list_states)


@app_views.route("states/<state_id>")
def get_state_by_id(state_id):
    'retrive an object into a json'

    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('states/<state_id>', methods=['DELETE'])
def delete_state_by_id(state_id):
    'retrive an object into a json'

    state = storage.get("State", state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
