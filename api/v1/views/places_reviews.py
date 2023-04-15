#!/usr/bin/python3
"""
Creates a view for Review object that handles all default RESTFul API actions
"""
from models.user import User
from models.review import Review
from models.place import Place
from models.state import State
from models.city import City
from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def list_reviews(place_id):
    state = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def list_a_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_dict = request.get_json()
    if not json_dict:
        abort(400, "Not a JSON")
    if "user_id" not in json_dict:
        abort(400, "Missing user_id")
    if 'text' not in json_dict:
        abort(400, description="Missing text")
    user = storage.get(User, json_dict.get("user_id"))
    if user is None:
        abort(404)
    new_review = Review(**json_dict)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    json_dict = request.get_json()
    if not json_dict:
        abort(400, "Not a JSON")

    for key, value in json_dict.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
