#!/usr/bin/python3
'states handling for api'
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.state import City


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city_by_id(city_id):
    'updates a city'
    if not request.get_json():
        abort(400, "Not a JSON")

    city = storage.get("City", city_id)

    if city:
        for key, value in request.get_json().items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(city, key, value)
        city.save()
    else:
        abort(404)

    return jsonify(city.to_dict()), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city_by_id(state_id):
    'create a city'
    if not request.get_json():
        abort(400, "Not a JSON")
    if not request.get_json().get("name"):
        abort(400, "Missing name")

    state = storage.get("State", state_id)

    if not state:
        abort(404)

    city = City(**request.get_json())
    setattr(city, 'state_id', state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/states/<state_id>/cities")
def cities(state_id):
    'Retrieves the list of all City objects of a State'
    cities_list = []
    state = storage.get("State", state_id)
    if state:
        for obj in state.cities:
            cities_list.append(obj.to_dict())
        return jsonify(cities_list)
    else:
        abort(404)


@app_views.route("/cities/<city_id>")
def get_city_by_id(city_id):
    'Retrieves a City object'

    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    'delete a city object'

    city = storage.get("City", city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
