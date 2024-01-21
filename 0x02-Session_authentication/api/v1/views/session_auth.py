#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, make_response, session, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['post'], strict_slashes=False)
def auth_session_login():
    """view for session login"""
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    if email == '':
        return jsonify({"error": "email missing"}), 400
    if password == '':
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if len(user) != 0:
        user = user[0]
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    session_name_env = os.getenv('SESSION_NAME')
    response = jsonify(user.to_json())
    response.set_cookie(session_name_env, session_id)
    return response


@app_views.route(
        '/auth_session/logout',
        methods=['delete'],
        strict_slashes=False)
def auth_session_logout():
    """view for session logout"""
    from api.v1.app import auth
    destroy = auth.destroy_session(request)
    if not destroy:
        abort(404)
    return jsonify({}), 200
