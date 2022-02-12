#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""
from models.city import City
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from flasgger.utils import swag_from


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@swag_from('docs/cities/get_city_by_state.yml', methods=['GET'])
def get_city_by_state(state_id):
    """return a list of cities based on state id"""
    state = storage.get(State, state_id)
    st_cities = []
    if not state:
        abort(404)
    for city in state.cities:
        st_cities.append(city.to_dict())
    return jsonify(st_cities), 200


@app_views.route('/cities', methods=['GET'],
                 strict_slashes=False)
@swag_from('docs/cities/cities.yml', methods=['GET'])
def cities():
    """Return all cities"""
    cities = [city.to_dict() for city in storage.all("City").values()]
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('docs/cities/get_city.yml', methods=['GET'])
def get_city(city_id):
    """city by id"""
    city = storage.get(City, city_id)
    if city is not None:
        city = city.to_dict()
        return jsonify(city), 200
    return abort(404)


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('docs/cities/del_city.yml', methods=['DELETE'])
def del_city(city_id):
    """Delete city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from('docs/cities/post_city.yml', methods=['POST'])
def post_city(state_id):
    """Create a city object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    jsn = request.get_json()
    obj = City(**jsn)
    setattr(obj, 'state_id', state_id)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('docs/cities/put_city.yml', methods=['PUT'])
def put_city(city_id):
    """Update a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict())
