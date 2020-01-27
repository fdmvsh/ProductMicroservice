from celery.schedules import crontab

BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = BROKER_URL

CELERYBEAT_SCHEDULE = {
    "bgjob.periodic_task-every-minute": {
        "task": "periodic_task",
        "schedule": crontab(minute="*"),
    }
}
