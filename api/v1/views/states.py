l#!/usr/bin/python3
'states handling for api'
from flask import jsonify


@app.route('/api/v1/states')
def state():
    'retrive an object into a json'
    return to_dict(States)


@app.route('/api/v1/states/:states_id')
def stateid(states_id):
    'retrive an object into a json'
    try:
        return get(State, states_id)
    except:
        raise error 404


@app.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete
