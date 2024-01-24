#!/usr/bin/env python3
"""test module"""

import requests

url = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """test register user route"""
    data = {'email': email, 'password': password}
    req = requests.post(f'{url}/users', data=data)
    expected_res = {
            "email": "guillaume@holberton.io",
            "message": "user created"
            }
    if req.status_code == 200:
        assert req.json() == expected_res
    else:
        assert req.status_code == 400
        assert req.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """log in with wrong password"""
    data = {'email': email, 'password': password}
    req = requests.post(f'{url}/sessions', data=data)
    assert req.status_code == 401


def log_in(email: str, password: str) -> str:
    """log a user in"""
    data = {'email': email, 'password': password}
    req = requests.post(f'{url}/sessions', data=data)

    assert req.status_code == 200
    assert req.json() == {"email": f"{email}", "message": "logged in"}
    return req.cookies['session_id']


def profile_unlogged() -> None:
    """access profile unlogged"""
    req = requests.get(f'{url}/profile')
    assert req.status_code == 403


def profile_logged(session_id: str) -> None:
    """access profile while logged in"""
    req = requests.get(f'{url}/profile', cookies={'session_id': session_id})
    assert req.status_code == 200
    assert req.json() == {'email': f'{EMAIL}'}


def log_out(session_id: str) -> None:
    """log out of the session"""
    req = requests.delete(f'{url}/sessions',
                          cookies={'session_id': session_id})

    assert req.status_code == 200


def reset_password_token(email: str) -> str:
    """reset password token"""
    data = {'email': email}
    req = requests.post(f'{url}/reset_password', data=data)

    if req.status_code == 200:
        reset_token = req.json()['reset_token']
        assert req.json() == {
                'email': f'{email}',
                'reset_token': f'{reset_token}'
                }
        return reset_token
    else:
        assert req.status_code == 403


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update password"""
    data = {
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password
            }
    req = requests.put(f'{url}/reset_password', data=data)

    if req.status_code == 200:
        assert req.json() == {
                "email": f"{email}",
                "message": "Password updated"
                }
    else:
        assert req.status_code == 403


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
