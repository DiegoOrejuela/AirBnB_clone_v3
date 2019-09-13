#!/usr/bin/python3
'amenities handling for api'
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


_cls = "Amenity"
path_folder = "amenities"
path_id = "amenity_id"


@app_views.route("/{}".format(path_folder))
def get_objects():
    """retrive an object into a json"""
    list_objects = []
    for key, value in storage.all(_cls).items():
        list_objects.append(value.to_dict())
    return jsonify(list_objects)


@app_views.route("{}/<{}>".format(path_folder, path_id))
def get_object_by_id(amenity_id):
    'retrive an object into a json'

    _object = storage.get(_cls, amenity_id)
    if _object:
        return jsonify(_object.to_dict())
    else:
        abort(404)


@app_views.route("{}/<{}>".format(path_folder, path_id), methods=['DELETE'])
def delete_object_by_id(amenity_id):
    'retrive an object into a json'

    _object = storage.get(_cls, amenity_id)
    if _object:
        storage.delete(_object)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/{}".format(path_folder), methods=['POST'])
def post_object():
    'retrive an object into a json'
    if not request.get_json():
        abort(400, "Not a JSON")
    if not request.get_json().get("name"):
        abort(400, "Missing name")

    _object = Amenity(**request.get_json())
    _object.save()
    return jsonify(_object.to_dict()), 201


@app_views.route("{}/<{}>".format(path_folder, path_id), methods=['PUT'])
def put_object_by_id(amenity_id):
    'retrive an object into a json'
    if not request.get_json():
        abort(400, "Not a JSON")

    _object = storage.get(_cls, amenity_id)

    if _object:
        for key, value in request.get_json().items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(_object, key, value)
        _object.save()
    else:
        abort(404)

    return jsonify(_object.to_dict()), 200
