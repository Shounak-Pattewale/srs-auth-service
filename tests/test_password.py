import pytest

from srs_auth.password import hash_password, verify_password


def test_hash_is_not_plaintext():
    hashed = hash_password("mysecret")
    assert hashed != "mysecret"


def test_correct_password_verifies():
    hashed = hash_password("correct-horse-battery-staple")
    assert verify_password("correct-horse-battery-staple", hashed) is True


def test_wrong_password_fails():
    hashed = hash_password("correct")
    assert verify_password("wrong", hashed) is False


def test_unique_hashes_per_call():
    h1 = hash_password("same")
    h2 = hash_password("same")
    assert h1 != h2


def test_empty_password():
    hashed = hash_password("")
    assert verify_password("", hashed) is True
    assert verify_password("notempty", hashed) is False
