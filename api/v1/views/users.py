#!/usr/bin/python3
'Place objects that handles all default RestFul API actions'
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.state import City
from models.place import Place
from models.user import User


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user_by_id(user_id):
    'updates a user'
    if not request.get_json():
        abort(400, "Not a JSON")

    users = storage.get("User", user_id)

    if users:
        for key, value in request.get_json().items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(users, key, value)
        users.save()
    else:
        abort(404)

    return jsonify(users.to_dict()), 200


@app_views.route('/users', methods=['POST'])
def post_user_by_id():
    'create a place'
    if not request.get_json():
        abort(400, "Not a JSON")
    if not request.get_json().get("email"):
        abort(400, "Missing email")
    if not request.get_json().get("password"):
        abort(400, "Missing password")

    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users")
def users():
    'Retrieves the list of all users'
    users_list = []
    for key, value in storage.all("User").items():
        users_list.append(value.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<user_id>")
def get_user_by_id(user_id):
    'Retrieves a user object'

    users = storage.get("User", user_id)
    if users:
        return jsonify(users.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_users_by_id(user_id):
    'delete a user object'

    users = storage.get("User", user_id)
    if users:
        storage.delete(users)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
