import time

import jwt
import pytest

from srs_auth.jwt_utils import create_token, decode_token

SECRET = "a-test-secret-key-that-is-long-enough-for-hs256"


def test_round_trip():
    token = create_token({"user_id": "abc", "role": "buyer"}, SECRET)
    payload = decode_token(token, SECRET)
    assert payload["user_id"] == "abc"
    assert payload["role"] == "buyer"


def test_exp_included():
    token = create_token({"user_id": "x"}, SECRET, expires_in=3600)
    payload = decode_token(token, SECRET)
    assert "exp" in payload


def test_expired_token_raises():
    token = create_token({"user_id": "x"}, SECRET, expires_in=1)
    time.sleep(2)
    with pytest.raises(jwt.ExpiredSignatureError):
        decode_token(token, SECRET)


def test_wrong_secret_raises():
    token = create_token({"user_id": "x"}, SECRET)
    with pytest.raises(jwt.InvalidTokenError):
        decode_token(token, "wrong-secret-key-that-is-also-long-enough")


def test_tampered_token_raises():
    token = create_token({"user_id": "x"}, SECRET)
    tampered = token[:-4] + "XXXX"
    with pytest.raises(jwt.InvalidTokenError):
        decode_token(tampered, SECRET)
