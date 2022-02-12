#!/usr/bin/python3
"""view for User objects that handles all default RESTFul API actions"""
from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('docs/users/users.yml', methods=['GET'])
def users():
    """return all users"""
    users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('docs/users/get_user.yml', methods=['GET'])
def get_user(user_id):
    """user by id"""
    user = storage.get(User, user_id)
    if user is not None:
        user = user.to_dict()
        return jsonify(user), 200
    return abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('docs/users/del_user.yml', methods=['DELETE'])
def del_user(user_id):
    """Delete user by id"""
    user = storage.get(User, user_id)
    if user is not None:
        user.delete()
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
@swag_from('docs/users/post_user.yml', methods=['POST'])
def post_user():
    """Create a object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "email" not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    elif "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    jsn = request.get_json()
    obj = User(**jsn)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('docs/users/put_user.yml', methods=['PUT'])
def put_user(user_id):
    """Update a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    elif not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'email' 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
