import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_service.settings")

app = Celery("site_service_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
