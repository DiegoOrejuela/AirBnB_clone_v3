#!/usr/bin/python3
'Place objects that handles all default RestFul API actions'
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.state import City
from models.place import Place


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place_by_id(place_id):
    'updates a place'
    if not request.get_json():
        abort(400, "Not a JSON")

    place = storage.get("Place", place_id)

    if place:
        for key, value in request.get_json().items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(place, key, value)
        place.save()
    else:
        abort(404)

    return jsonify(place.to_dict()), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place_by_id(city_id):
    'create a place'
    if not request.get_json():
        abort(400, "Not a JSON")
    if not request.get_json().get("name"):
        abort(400, "Missing name")
    if not request.get_json().get("user_id"):
        abort(400, "Missing user_id")

    city = storage.get("City", city_id)
    if not storage.get("User", request.get_json().get("user_id")):
        abort(400)

    if not city:
        abort(400)

    place = Place(**request.get_json())
    setattr(place, 'city_id', city_id)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/cities/<city_id>/places")
def places(city_id):
    'Retrieves the list of all places objects of a city'
    places_list = []
    city = storage.get("City", city_id)
    if city:
        for obj in city.places:
            places_list.append(obj.to_dict())
        return jsonify(places_list)
    else:
        abort(404)


@app_views.route("/places/<place_id>")
def get_places_by_id(place_id):
    'Retrieves a place object'

    place = storage.get("Place", place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_by_id(place_id):
    'delete a place object'

    place = storage.get("Place", place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
