#!/usr/bin/env python3
"""a module that implements a Basic auth"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """A subclass of the Auth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Base64 part of the Authorization header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if isinstance(authorization_header, str) is False:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Decode a base64 string"""
        if base64_authorization_header is None:
            return None
        if isinstance(base64_authorization_header, str) is False:
            return None
        try:
            return base64.b64decode(
                    base64_authorization_header.encode('utf-8')
                    ).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """return user credentials"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if isinstance(decoded_base64_authorization_header, str) is False:
            return (None, None)
        if ':' in decoded_base64_authorization_header:
            email, passwd = decoded_base64_authorization_header.split(':')
            return (email, passwd)
        return (None, None)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """return user object"""
        if user_email is None or type(user_email) is str:
            return None
        if user_pwd is None or type(user_pwd) is str:
            return None
        user = User()
        yy = user.search({'email': user_email})
        if len(yy) == 0:
            return None
        user = yy[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user
