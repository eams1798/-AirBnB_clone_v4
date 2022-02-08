#!/usr/bin/python3
"""cities API blueprint"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def state_cities():
    """Return status ok"""
    return jsonify({'status': 'ok'})


@app_views.route('/api/v1/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def state_cities():
    """Return status ok"""
    return jsonify({'status': 'ok'})


@app_views.route('/stats', strict_slashes=False)
def count():
    """Return count"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
