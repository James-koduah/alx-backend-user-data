#!/usr/bin/env python3
"""authentication mehtods"""

import bcrypt
from db import DB
from user import User
import uuid


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

    def valid_login(self, email: str, password: str) -> bool:
        """check if credientials are valid"""
        try:
            user = self._db.find_user_by(email=email)
            a = bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
            return a
        except Exception as e:
            return False

    def create_session(self, email: str) -> str:
        """create or return a new session id"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            return None

        if user.session_id:
            return str(user.session_id)
        else:
            self._db.update_user(
                    user.id,
                    session_id=_generate_uuid()
                    )
            return str(user.session_id)

    def get_user_from_session_id(self, session_id: str) -> User:
        """get a user by session"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy a users session"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except Exception as e:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """update the user's reset_token field"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            raise ValueError
        self._db.update_user(user.id, reset_token=_generate_uuid())
        return str(user.reset_token)

    def update_password(self, reset_token: str, password: str) -> None:
        """update a users password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception as e:
            raise ValueError()

        hashed_password = _hash_password(password)
        self._db.update_user(
                user.id,
                hashed_password=hashed_password,
                reset_token=None
                )
        return None


def _hash_password(password: str) -> bytes:
    """hash a password"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes, salt)
    return hashed_password


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())
