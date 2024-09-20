#!/usr/bin/python3
"""
views for amenities page
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review

classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}

@app_views.route('/amenities', strict_slashes=False)
def list_amenities():
    amenities = storage.all(Amenity)
    amenity_list = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenity_list)
    