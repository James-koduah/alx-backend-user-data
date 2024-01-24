#!/usr/bin/env python3
"""flask app"""

from flask import Flask, request, jsonify, abort, redirect
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


@app.route('/sessions', methods=['delete'], strict_slashes=False)
def logout():
    """log a user out and destroy session"""
    session_id = request.cookies.get('session_id', '')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', strict_slashes=False)
def profile():
    """a user's profile"""
    session_id = request.cookies.get('session_id', '')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({'email': f'{user.email}'})
    else:
        abort(403)


@app.route('/reset_password', methods=['post'], strict_slashes=False)
def get_reset_password_token():
    """send a reset password token"""
    email = request.form.get('email', '')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({'email': f'{email}', 'reset_token': f'{reset_token}'})
    except Exception as e:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
