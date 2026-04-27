from datetime import datetime, timedelta, timezone

import jwt


def create_token(payload: dict, secret_key: str, expires_in: int = 3600) -> str:
    data = payload.copy()
    data["exp"] = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    return jwt.encode(data, secret_key, algorithm="HS256")


def decode_token(token: str, secret_key: str) -> dict:
    return jwt.decode(token, secret_key, algorithms=["HS256"])
