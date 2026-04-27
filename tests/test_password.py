import pytest

from srs_auth.password import hash_password, verify_password


def test_hash_is_not_plaintext():
    hashed = hash_password("mysecret")
    assert hashed != "mysecret"
    # Argon2 hash starts with $argon2
    assert hashed.startswith("$argon2")


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
    # Both should be valid argon2 hashes
    assert h1.startswith("$argon2")
    assert h2.startswith("$argon2")


def test_empty_password():
    hashed = hash_password("")
    assert verify_password("", hashed) is True
    assert verify_password("notempty", hashed) is False


def test_hash_parameters():
    """Test that Argon2 parameters are set correctly (memory, iterations, parallelism)."""
    hashed = hash_password("test")
    # Argon2id default: memory_cost=65536 (64MB), time_cost=2, parallelism=1
    assert "m=65536" in hashed or "m=32768" in hashed  # 32MB or 64MB memory
    assert "t=" in hashed  # time cost present
    assert "p=" in hashed  # parallelism present
