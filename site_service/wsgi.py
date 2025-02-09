import os

from decouple import config
from django.core.wsgi import get_wsgi_application

from core.enums import Environment

environment = config("ENVIRONMENT", default=Environment.PROD.value)

if environment == Environment.PROD.value:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_service.settings.prod")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_service.settings.dev")

application = get_wsgi_application()
