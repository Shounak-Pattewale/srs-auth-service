from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash, VerificationError


ph = PasswordHasher()


def hash_password(plain: str) -> str:
    """Hash a password using Argon2id (industry standard)."""
    return ph.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a password against a hash using Argon2id."""
    try:
        ph.verify(hashed, plain)
        return True
    except (VerifyMismatchError, InvalidHash, VerificationError):
        return False
