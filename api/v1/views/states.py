#!/usr/bin/python3
"""
views for state page
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


@app_views.route('/states', strict_slashes=False)
def states():
    """list all states"""
    state_list = []
    all_states = storage.all(classes["states"])
    for value in all_states.values():
        state_list.append(value.to_dict())
    
    return jsonify(state_list)

@app_views.route('/states/<state_id>', strict_slashes=False)
def state_id(state_id):
    """Get state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods = ['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods = ['POST'], strict_slashes=False)
def add_state():
    """Create State"""
    # Get the JSON data from the request
    data = request.get_json()
    
    # Check if the request body is valid JSON
    if data is None:
        abort(400, description="Not a JSON")
    
    # Check if 'name' is in the request data
    if 'name' not in data:
        abort(400, description="Missing name")
        
    # Check if a state with this name already exists
    all_states = storage.all(State)
    all_list = [value for value in all_states.values()]
    for all in all_list:
        if all.name == data['name']:
            abort(409, description="State with this name already exists")
    
    # Create a new State object
    new_state = State(**data)
    
    # Save the new State to the storage
    storage.new(new_state)
    storage.save()
    
    # Return the new State as JSON with status code 201
    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods = ['PUT'], strict_slashes =True)
def update_state(state_id):
    """Update state"""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
            
    storage.save()    
    # Return the State object with the status code 200
    return jsonify(state.to_dict()), 200
    
    


