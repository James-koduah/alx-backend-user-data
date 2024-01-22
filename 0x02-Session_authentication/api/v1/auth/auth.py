#!/usr/bin/env python3
"""An authentication module"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """An authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth return false"""
        if path is None:
            return True

        wildcard_paths = []
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*':
                wildcard_paths.append(excluded_path[0:-1])

        if path[-1] != '/':
            path = path + '/'

        if excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        if wildcard_paths != []:
            for excluded_path in wildcard_paths:
                if path.startswith(excluded_path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """The flask authorization header"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """get the current user"""
        return None

    def session_cookie(self, request=None):
        """Get cookies"""
        if not request:
            return None
        cookie_name = os.getenv('SESSION_NAME')
        cookie = request.cookies.get(cookie_name, None)
        return cookie
