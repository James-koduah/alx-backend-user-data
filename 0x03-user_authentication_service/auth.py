#!/usr/bin/env python3
"""authentication mehtods"""

import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user"""
        try:
            self._db.find_user_by(email=email)
        except Exception as e:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError(f'User {email} already exists')


def _hash_password(password: str) -> bytes:
    """hash a password"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes, salt)
    return hashed_password
