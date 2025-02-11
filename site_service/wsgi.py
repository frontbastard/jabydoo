import os

from decouple import config
from django.core.wsgi import get_wsgi_application

environment = config("ENVIRONMENT")

if environment == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_service.settings.prod")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_service.settings.dev")

application = get_wsgi_application()
