import pytest


async def _get_token(client):
    resp = await client.post(
        "/api/auth/register",
        json={"email": "tasker@example.com", "password": "Secret123!", "org_name": "Tasks"},
    )
    return resp.json()["tokens"]["access_token"]


@pytest.mark.asyncio
async def test_task_crud(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    created = await client.post(
        "/api/tasks/",
        json={"title": "Draft proposal", "description": "Outline scope"},
        headers=headers,
    )
    assert created.status_code == 200
    task_id = created.json()["id"]

    updated = await client.patch(
        f"/api/tasks/{task_id}",
        json={"status": "in_progress"},
        headers=headers,
    )
    assert updated.status_code == 200

    listed = await client.get("/api/tasks/?limit=10", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    deleted = await client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert deleted.status_code == 200
