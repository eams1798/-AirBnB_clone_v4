#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """return all states"""
    states = [state.to_dict() for state in storage.all("State").values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """state by id"""
    state = storage.get(State, state_id)
    if state is not None:
        state = state.to_dict()
        return jsonify({state}), 200
    return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """Delete state by id"""
    state = storage.get(State, state_id)
    if state is not None:
        state.delete()
        storage.save()
        return jsonify({})
    return abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post():
    """Create a object"""
    if not request_json:
        return jsonify({"error": "Not a JSON"}), 404
    elif "name" not in request_json:
        return make_response(jsonify({"error": "Missing name"}), 404)
    jsn = request.get_json()
    obj = State(**jsn)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put(state_id):
    """Update a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    elif not request.get_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
