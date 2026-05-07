import pytest


async def _get_token(client):
    resp = await client.post(
        "/api/auth/register",
        json={"email": "invoice@example.com", "password": "Secret123!", "org_name": "Invoices"},
    )
    return resp.json()["tokens"]["access_token"]


@pytest.mark.asyncio
async def test_invoice_status_transition(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    created = await client.post(
        "/api/invoices/",
        json={"title": "April Retainer", "amount": 1200, "currency": "BDT"},
        headers=headers,
    )
    assert created.status_code == 200
    invoice_id = created.json()["id"]

    updated = await client.patch(
        f"/api/invoices/{invoice_id}",
        json={"status": "paid"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "paid"
