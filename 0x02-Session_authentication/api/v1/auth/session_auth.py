#!/usr/bin/env python3
"""a module that implements Session auth"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """A subclass of the Auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create a session id for user_id"""
        if not user_id or type(user_id) is not str:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """return a user_id based on a session id"""
        if not session_id or type(session_id) is not str:
            return None
        user_id = self.user_id_by_session_id.get(session_id, None)
        return user_id
