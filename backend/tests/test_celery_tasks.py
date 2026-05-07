import pytest
from workers import webhook_worker
from workers import overdue_worker


def test_deliver_webhook_retries(monkeypatch):
    calls = {"count": 0}

    async def _fail(*_args, **_kwargs):
        calls["count"] += 1
        raise RuntimeError("boom")

    monkeypatch.setattr(webhook_worker, "_deliver_for_org", _fail)

    with pytest.raises(Exception):
        webhook_worker.deliver_webhook.run(org_id=1, event="task.created", payload={})


def test_overdue_task_runs(monkeypatch):
    async def _fake_mark_overdue():
        return 2

    monkeypatch.setattr(overdue_worker, "_mark_overdue", _fake_mark_overdue)
    assert overdue_worker.daily_overdue_check() == 2
