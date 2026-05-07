import os
from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
TIMEZONE = os.getenv("TIMEZONE", "UTC")

celery_app = Celery(
    "taskflow_ai",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "workers.webhook_worker",
        "workers.overdue_worker",
        "workers.digest_worker",
    ],
)

celery_app.conf.timezone = TIMEZONE
celery_app.conf.beat_schedule = {
    "daily-overdue-check": {
        "task": "workers.overdue_worker.daily_overdue_check",
        "schedule": crontab(hour=9, minute=0),
    },
    "weekly-digest": {
        "task": "workers.digest_worker.weekly_digest",
        "schedule": crontab(hour=8, minute=0, day_of_week=1),
    },
}
