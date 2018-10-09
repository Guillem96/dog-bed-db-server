import pytest
import json


def test_sign_up(auth):
    # Correct signup
    res = auth.sign_up("Guillem", "Orellana", "guillem",
                       "pw", "guillem@email.com")
    res_data = json.loads(res.data)
    assert res.status_code == 201
    assert res_data["username"] == "guillem" and res_data["first_name"] == "Guillem"

    # User already exists
    res = auth.sign_up("Guillem", "Orellana", "guillem",
                       "pw", "guillem@email.com")
    res_data = json.loads(res.data)
    assert "already exists" in res_data["msg"]
    assert res.status_code == 400

    # Properties cannot be blank
    res = auth.sign_up("Guillem", "Orellana", "guillem",
                       "", "guillem@email.com")
    res_data = json.loads(res.data)
    assert "cannot be blank" in res_data["msg"]
    assert res.status_code == 400


def test_login(auth):
    # Correct signup
    res = auth.sign_up("Guillem", "Orellana", "guillem",
                       "pw", "guillem@email.com")
    assert res.status_code == 201

    # Correct login
    res = auth.login("guillem", "pw")
    assert res.status_code == 200

    # Forbidden
    res = auth.login("guillem", "incorrect")
    assert res.status_code == 401

    # Get the identity
    res = auth.identity("guillem", "pw")
    res_data = json.loads(res.data)
    assert res_data["email"] == "guillem@email.com"
    assert res_data["username"] == "guillem"

    # Non existent user identity
    res = auth.identity("non_existent", "pw")
    assert res.status_code == 401
