from celery import Celery
import os

app = Celery("worker_scraper")

# Load configuration from the config module
app.config_from_object("apps.worker_scraper.celery_config")

# Ensure tasks are discovered
app.autodiscover_tasks(["apps.worker_scraper"])

