#!/usr/bin/python3
"""
Creates a view for Review object that handles all default RESTFul API actions
"""
from models.place import Place
from models.amenity import Amenity
from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import request, jsonify, abort
from os import getenv

mode = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def list_amenities_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if mode == 'db':
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        return jsonify([
            storage.get(Amenity, amenity_id).to_dict
            for amenity_id in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if mode == 'db':
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity not in place.amenity_id:
            abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_amenity_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if mode == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        else:
            place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_id:
            return jsonify(amenity.to_dict())
        else:
            place.amenity_id.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
