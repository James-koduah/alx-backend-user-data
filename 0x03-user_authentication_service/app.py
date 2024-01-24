#!/usr/bin/env python3
"""flask app"""

from flask import Flask, request, jsonify, abort
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def home():
    """base route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['post'], strict_slashes=False)
def users():
    """function for users"""
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": f"{user.email}",
            "message": "user created"
            })
    except Exception as e:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['post'], strict_slashes=False)
def login():
    """log a user in with a new session"""
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    if AUTH.valid_login(email, password):
        new_session = AUTH.create_session(email)
        response = jsonify({
            "email": f"{email}",
            "message": "logged in"
            })
        response.set_cookie('session_id', new_session)
        return response
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
