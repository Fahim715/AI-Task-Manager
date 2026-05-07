import hmac
import hashlib
import json

from services.webhook import sign_payload


def test_webhook_signature():
    secret = "whsec_test"
    payload = {"event": "task.created", "task_id": 123}

    signature = sign_payload(secret, payload)
    expected_raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    expected = hmac.new(secret.encode("utf-8"), expected_raw, hashlib.sha256).hexdigest()

    assert signature == f"sha256={expected}"
