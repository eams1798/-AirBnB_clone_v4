#!/usr/bin/python3
"""object app_views that returns a JSON: status: OK"""
from flask import jsonify
from flask import Flask
from api.v1.views import app_views


app_views.url_map.strict_slashes = False


@app_views.route('/status')
def status():
    """Return status ok"""
    return jsonify({'status': 'ok'})
