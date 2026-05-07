import pytest


@pytest.mark.asyncio
async def test_auth_flow(client):
    register = await client.post(
        "/api/auth/register",
        json={"email": "user@example.com", "password": "Secret123!", "org_name": "Acme"},
    )
    assert register.status_code == 200
    data = register.json()
    assert data["tokens"]["access_token"]
    assert data["tokens"]["refresh_token"]

    login = await client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "Secret123!"},
    )
    assert login.status_code == 200
    login_data = login.json()
    refresh = await client.post(
        "/api/auth/refresh",
        json={"refresh_token": login_data["tokens"]["refresh_token"]},
    )
    assert refresh.status_code == 200
    assert refresh.json()["access_token"]
