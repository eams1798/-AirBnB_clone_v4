#!/usr/bin/python3
"""object app_views that returns a JSON: status: OK"""
from flask import jsonify
from flask import Flask
from api.v1.views import app_views
from models import storage
from flasgger.utils import swag_from


@app_views.route('/status', strict_slashes=False)
@swag_from('docs/status.yml', methods=['GET'])
def status():
    """Return status ok"""
    return jsonify({'status': 'ok'})


@app_views.route('/stats', strict_slashes=False)
@swag_from('docs/stats.yml', methods=['GET'])
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
