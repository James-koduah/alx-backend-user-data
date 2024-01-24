#!/usr/bin/env python3
"""authentication mehtods"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """hash a password"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes, salt)
    return hashed_password
