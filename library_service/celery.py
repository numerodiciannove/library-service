import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")

app = Celery("library_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

from celery.schedules import crontab

app.conf.beat_schedule = {
    "send_daily_at_12": {
        "task": "borrowings_app.tasks.send_overdue_message",
        "schedule": crontab(hour=12, minute=30, day_of_week="*"),
    },
}
