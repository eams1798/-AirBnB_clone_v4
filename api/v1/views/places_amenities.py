#!/usr/bin/python3
"""
This file contains the Amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity
from models.user import User


@app_views.route('/places/<string:place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities_by_place(place_id):
    """ get amenities from a spcific place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not place.amenities:
        return jsonify([])
    amenities = [obj.to_dict() for obj in place.amenities]
    return jsonify(amenities)


@app_views.route('/amenities/<string:place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amen_place(place_id, amenity_id):
    """ delete amenity by place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_obj_amen_place(place_id, amenity_id):
    """ create new instance """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
    return jsonify(amenity.to_dict()), 200
