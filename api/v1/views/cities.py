#!/usr/bin/python3
"""
views for cities page
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

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=True)
def get_cities(state_id):
    all_cities = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404, description="no state found")
    cities = state.cities
    for city in cities:
        city = city.to_dict()
        all_cities.append(city)
    return jsonify(all_cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=True)
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city = city.to_dict()
    return jsonify(city)

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=True)
def delete_city(city_id):
    """Delete city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=True)
def create_city(state_id):
    """Create a City"""
    data = request.get_json()
    if data is None:
        abort(404, description="Not a JSON")
    if "name" not in data:
        abort(404, description="Missing Name")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities_list = state.cities
    if data["name"] in cities_list:
        abort(409, description="already exists")
        
    data['state_id'] = state_id
    new_city = City(**data)
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=True)
def update_city(city_id):
    city = storage.get(City, city_id)
    data = request.get_json()
    if city is None:
        abort(404)
    if data is None:
        abort(404, description="Not a JSON")
    for key, value in data.items():
        if key not in ["id","state_id","created_at","updated_at"]:
            setattr(city,key,value)
    city.save()
    storage.save()
    return jsonify(city.to_dict()), 200
    
    
    


    

    
