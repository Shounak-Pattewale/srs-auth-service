import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from srs_auth import create_token, make_get_current_user, make_require_role
from srs_auth.middleware import make_role_guard, make_tenant_guard

SECRET = "a-test-secret-key-that-is-long-enough-for-hs256"
get_current_user = make_get_current_user(SECRET)
require_admin = make_require_role("admin", "super_admin")
admin_guard = make_role_guard(SECRET, "admin")
tenant_guard = make_tenant_guard(SECRET)

app = FastAPI()


@app.get("/me")
async def me(user=__import__("fastapi").Depends(get_current_user)):
    return user


@app.get("/admin")
async def admin(user=__import__("fastapi").Depends(admin_guard)):
    return user


client = TestClient(app, raise_server_exceptions=False)


def _token(role="buyer", tenant_id="t1"):
    return create_token({"user_id": "u1", "role": role, "tenant_id": tenant_id}, SECRET)


def test_valid_token_returns_user():
    r = client.get("/me", headers={"Authorization": f"Bearer {_token()}"})
    assert r.status_code == 200
    assert r.json()["user_id"] == "u1"


def test_missing_token_returns_401():
    r = client.get("/me")
    assert r.status_code == 401


def test_invalid_token_returns_401():
    r = client.get("/me", headers={"Authorization": "Bearer not.a.token"})
    assert r.status_code == 401


def test_role_guard_allows_correct_role():
    r = client.get("/admin", headers={"Authorization": f"Bearer {_token(role='admin')}"})
    assert r.status_code == 200


def test_role_guard_blocks_wrong_role():
    r = client.get("/admin", headers={"Authorization": f"Bearer {_token(role='buyer')}"})
    assert r.status_code == 403
