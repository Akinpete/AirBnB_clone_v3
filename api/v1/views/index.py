#!/usr/bin/python3
"""
views for home/index page
"""
from flask import Flask, Blueprint, jsonify
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


@app_views.route('/status', strict_slashes=False)
def hbnbStatus():
    """hbnbStatus"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def hbnbStats():
    """hbnbStats"""
    return_dict = {}
    for key, value in classes.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)

