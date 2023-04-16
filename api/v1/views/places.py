#!/usr/bin/python3
"""
Creates a view for State objects that handles all default RESTFul API actions
"""
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_place_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def list_a_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_dict = request.get_json()
    if not json_dict:
        abort(400, description="Not a JSON")
    if not json_dict.get("user_id"):
        abort(400, description="Missing user_id")
    if 'name' not in json_dict:
        abort(400, description="Missing name")
    user = storage.get(User, json_dict.get("user_id"))
    if user is None:
        abort(404)
    new_place = Place(**json_dict)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    json_dict = request.get_json()
    if not json_dict:
        abort(400, description="Not a JSON")

    for key, value in json_dict.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def search_places():
    request_body = request.get_json()
    if type(request_body) != dict:
        abort(400, description="Not a JSON")
    state_ids = request_body.get("states", [])
    city_ids = request_body.get("cities", [])
    amenity_ids = request_body.get("amenities", [])

    found_places = []

    if state_ids == city_ids == []:
        found_places = storage.all(Place).values()
    else:
        states = [
            storage.get(State, state_id) for state_id in state_ids
            if storage.get(State, state_id)
        ]
        cities = [city for state in states for city in state.cities]
        cities += [
            storage.get(City, city_id) for city_id in city_ids
            if storage.get(City, city_id)
        ]
        unique_cities = list(set(cities))
        found_places = [
            place for city in unique_cities for place in city.places]

    amenities = [
        storage.get(Amenity, amenity_id) for amenity_id in amenity_ids
        if storage.get(Amenity, amenity_id)
    ]

    result = []
    for place in found_places:
        result.append(place.to_dict())
        for amenity in amenities:
            if amenity not in place.amenities:
                result.pop()
                break

    return jsonify(result)
