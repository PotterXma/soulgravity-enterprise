from celery import Celery
import os

broker = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/2")
backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")

app = Celery("worker_publisher", broker=broker, backend=backend)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    include=["apps.worker_publisher.tasks.publish"]
)
