import os

from django.conf import settings
from django.core.asgi import get_asgi_application

from core.enums import Environment

environment = settings.ENVIRONMENT

if environment == Environment.PROD.value:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_service.settings.prod")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_service.settings.dev")

application = get_asgi_application()
