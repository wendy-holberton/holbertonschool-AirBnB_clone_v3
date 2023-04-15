#!/usr/bin/python3
"""
Create a new view for Amenity objects that handles all default RESTFul API
actions
"""

from models.amenity import Amenity
from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenities():
    amenities_list = []
    for value in storage.all(Amenity).values():
        amenities_list.append(value.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def list_an_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    json_dict = request.get_json()
    if not json_dict:
        abort(400, "Not a JSON")
    if 'name' not in json_dict:
        abort(400, "Missing name")
    new_amenity = Amenity(**json_dict)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    json_dict = request.get_json()
    if not json_dict:
        abort(400, "Not a JSON")

    for key, value in json_dict.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
