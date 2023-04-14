#!/usr/bin/python3
"""
Creates a view for State objects that handles all default RESTFul API actions
"""
from models.state import State
from models.state import City
from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def list_cities(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def list_a_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_dict = request.get_json()
    if not json_dict:
        abort(400, description="Not a JSON")
    if 'name' not in json_dict:
        abort(400, description="Missing name")
    new_city = City(**json_dict)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    json_dict = request.get_json()
    if not json_dict:
        abort(400, description="Not a JSON")

    for key, value in json_dict.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
