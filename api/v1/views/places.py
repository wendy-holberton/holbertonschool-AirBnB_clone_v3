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


@app_views.route('/cities/<city_id>/palces', methods=['GET'],
                 strict_slashes=False)
def list_place_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    place_list = []
    for place in city.places:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def list_a_place(palce_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_placey(place_id):
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
    if 'name' not in json_dict:
        abort(400, description="Missing name")
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
        if key not in ["id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
