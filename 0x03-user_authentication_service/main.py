#!/usr/bin/env python3
"""test module"""

import requests


def register_user(email: str, password: str) -> None:
    """test register user route"""
    data = {'email': email, 'password': password}
    req = requests.post('http://localhost:5000/users', data=data)
    expected_res = {
            "email": "guillaume@holberton.io",
            "message": "user created"
            }
    assert req.json() == expected_res


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
