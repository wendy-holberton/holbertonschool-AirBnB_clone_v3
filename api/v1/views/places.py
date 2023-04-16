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


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    body = request.get_json()
    if not isinstance(body, dict):
        abort(400, description="Not a JSON")
    id_states = body.get("states", [])
    id_cities = body.get("cities", [])
    id_amenities = body.get("amenities", [])
    states = [storage.get(State, _id)
              for _id in id_states if storage.get(State, _id)]
    cities = [storage.get(City, _id)
              for _id in id_cities if storage.get(City, _id)]

    if states and cities:
        cities = list(set(states[0].cities) & set(cities))
    elif states:
        cities = states[0].cities
    elif cities:
        pass
    else:
        return jsonify([place.to_dict()
                        for place in storage.all(Place).values()])

    amenities = [storage.get(Amenity, _id)
                 for _id in id_amenities if storage.get(Amenity, _id)]
    places = [place for place in storage.all(Place).values() if set(
        amenities).issubset(set(place.amenities)) and place.city in cities]

    return jsonify([place.to_dict() for place in places])
