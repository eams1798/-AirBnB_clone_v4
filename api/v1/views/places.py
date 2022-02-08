#!/usr/bin/python3
"""view for Place objects that handles all default RESTFul API actions"""
from models.place import Place
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def places():
    """return all places"""
    places = [place.to_dict() for place in storage.all("Place").values()]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """place by id"""
    place = storage.get(Place, place_id)
    if place is not None:
        place = place.to_dict()
        return jsonify(place), 200
    return abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(place_id):
    """Delete place by id"""
    place = storage.get(Place, place_id)
    if place is not None:
        place.delete()
        storage.save()
        return jsonify({})
    return abort(404)


@app_views.route('/places', methods=['POST'],
                 strict_slashes=False)
def post():
    """Create a object"""
    if not request_json:
        return jsonify({"error": "Not a JSON"}), 404
    elif "name" not in request_json:
        return make_response(jsonify({"error": "Missing name"}), 404)
    jsn = request.get_json()
    obj = Place(**jsn)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put(place_id):
    """Update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    elif not request.get_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())
