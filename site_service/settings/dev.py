from decouple import config

from .base import *

SECRET_KEY = config("DJANGO_SECRET_KEY", default="development-secret-key")

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS += [
    "sass_processor",
    "django_browser_reload",
]

MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATICFILES_FINDERS += [
    "sass_processor.finders.CssFinder",
]


SASS_PROCESSOR_ROOT = BASE_DIR / "static"
# SASS_PROCESSOR_INCLUDE_DIRS = [BASE_DIR / "node_modules"]
SASS_PROCESSOR_ENABLED = True
SASS_PROCESSOR_AUTO_INCLUDE = False
