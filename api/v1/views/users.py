#!/usr/bin/python3
"""
Creates a view for User objects that handles all default RESTFul API actions
"""
from models.base_model import BaseModel
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def list_users():
    users_list = []
    for value in storage.all(User).values():
        users_list.append(value.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def list_a_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    json_dict = request.get_json()
    if not json_dict:
        abort(400, "Not a JSON")
    if 'email' not in json_dict:
        abort(400, "Missing email")
    if 'password' not in json_dict:
        abort(400, "Missing passord")
    new_user = User(**json_dict)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    json_dict = request.get_json()
    if not json_dict:
        abort(400, "Not a JSON")

    for key, value in json_dict.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
