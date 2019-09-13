#!/usr/bin/python3
'Place objects that handles all default RestFul API actions'
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.state import City
from models.place import Place
from models.review import Review


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review_by_id(review_id):
    'updates a review'
    if not request.get_json():
        abort(400, "Not a JSON")

    review = storage.get("Review", review_id)

    if review:
        for key, value in request.get_json().items():
            if key != "id" and key != "created_at" and key != "updated_at"
            setattr(review, key, value)
        review.save()
    else:
        abort(404)

    return jsonify(review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review_by_id(place_id):
    'create a review'
    if not request.get_json():
        abort(400, "Not a JSON")
    if not request.get_json().get("name"):
        abort(400, "Missing name")
    if not request.get_json().get("user_id"):
        abort(400, "Missing user_id")

    place = storage.get("Place", place_id)
    if not storage.get("User", user_id):
        abort(400)

    if not place:
        abort(400)

    review = Review(**request.get_json())
    setattr(review, 'place_id', place_id)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/states/<place_id>/reviews")
def reviews(city_id):
    'Retrieves the list of all review objects of a city'
    reviews_list = []
    places = storage.get("Place", place_id)
    if places:
        for obj in places.reviews:
            reviews_list.append(obj.to_dict())
        return jsonify(reviews_list)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>")
def get_reviews_by_id(reviews_id):
    'Retrieves a reviews object'

    review = storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_place_by_id(review_id):
    'delete a review object'

    review = storage.get("Review", review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
