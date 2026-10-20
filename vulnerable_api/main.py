from typing import Optional
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(
    title="AgentSec Vulnerable API",
    description="Intentionally vulnerable API for local security testing.",
    version="1.0.0",
)

USERS = {
    "alice-token": {
        "id": 1,
        "username": "alice",
        "role": "user",
        "balance": 2500,
    },
    "bob-token": {
        "id": 2,
        "username": "bob",
        "role": "user",
        "balance": 7800,
    },
    "admin-token": {
        "id": 3,
        "username": "admin",
        "role": "admin",
        "balance": 15000,
    },
}


def authenticate(authorization: Optional[str]):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.removeprefix("Bearer ")

    user = USERS.get(token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user


@app.get("/")
def home():
    return {"message": "AgentSec Vulnerable API"}


@app.get("/api/me")
def get_me(authorization: Optional[str] = Header(default=None)):
    return authenticate(authorization)


@app.get("/api/users/{user_id}")
def get_user(
    user_id: int,
    authorization: Optional[str] = Header(default=None),
):
    authenticate(authorization)

    # VULNERABILITY: Missing object-level authorization.
    for user in USERS.values():
        if user["id"] == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


@app.get("/api/admin/stats")
def admin_stats(authorization: Optional[str] = Header(default=None)):
    authenticate(authorization)

    # VULNERABILITY: No admin role verification.
    return {
        "total_users": len(USERS),
        "revenue": 125000,
        "internal": True,
    }
