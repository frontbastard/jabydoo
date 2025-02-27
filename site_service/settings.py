import os
from pathlib import Path

from decouple import config
from django.utils.translation import gettext_lazy as _

from core.enums import Environment

SITE_TYPE = "health"

SITE_ID = 1
SITE_DOMAIN = config("SITE_DOMAIN")
SITE_NAME = config("SITE_NAME", default=SITE_DOMAIN)

BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = config("ENVIRONMENT", default=Environment.DEV.value)
DEBUG = config("DJANGO_DEBUG", "True") == "True"

SECRET_KEY = config("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="127.0.0.1").split(",")
CSRF_TRUSTED_ORIGINS = config("DJANGO_TRUSTED_ORIGINS").split(",")

# General settings
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",

    "imagekit",
    "django_ckeditor_5",
    "rosetta",
    "parler",
    "easy_thumbnails",
    "filer",
    "mptt",
    "compressor",
    "django_ace",

    "core.apps.CoreConfig",
    "pages.apps.PagesConfig",
    "seo.apps.SeoConfig",
    "menu.apps.MenuConfig",
    "games.apps.GamesConfig",
]

if ENVIRONMENT == Environment.DEV.value:
    INSTALLED_APPS += [
        "django_browser_reload",
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "core.middleware.UpdateSiteDomainMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if ENVIRONMENT == Environment.DEV.value:
    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]

ROOT_URLCONF = "site_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "templates" / SITE_TYPE,
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.language_flag_map",
                "core.context_processors.site_options",
            ],
        },
    },
]

WSGI_APPLICATION = "site_service.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Database
DATABASES = {
    "default": {
        "ENGINE": config("POSTGRES_ENGINE", "django.db.backends.sqlite3"),
        "NAME": config("POSTGRES_DB", BASE_DIR / "db.sqlite3"),
        "USER": config("POSTGRES_USER", default="user"),
        "PASSWORD": config("POSTGRES_PASSWORD", default="password"),
        "HOST": config("POSTGRES_HOST", default="localhost"),
        "PORT": config("POSTGRES_PORT", default="5432"),
    }
}

# International settings
LANGUAGE_CODE = "de"
LANGUAGES = [
    ("de", _("German")),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

PARLER_LANGUAGES = {
    1: (
        {"code": "de"},
    ), "default": {
        "fallback": "de",
        "hide_untranslated": False,
    }
}

# LANGUAGE_FLAG_MAP = {
#     "en": "en",
# }

TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "templates" / SITE_TYPE / "static",
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

COMPRESS_ENABLED = True
COMPRESS_REBUILD_TIMEOUT = 0
COMPRESS_OFFLINE = False
COMPRESS_PRECOMPILERS = [
    ("text/x-scss", "pysassc {infile} {outfile}"),
]

# Media files
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

FILER_STORAGES = {
    "public": {
        "main": {
            "ENGINE": "filer.storage.PublicFileSystemStorage",
            "OPTIONS": {
                "location": os.path.join(MEDIA_ROOT, "filer"),
                "base_url": "/media/filer/",
            },
        },
    },
}

THUMBNAIL_EXTENSION = "webp"
THUMBNAIL_TRANSPARENCY_EXTENSION = "webp"
THUMBNAIL_PRESERVE_EXTENSIONS = ["webp"]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CKEditor config
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": ["heading", "|", "bold", "italic", "link",
                    "bulletedList", "numberedList", "blockQuote", "imageUpload", ],

    },
    "extends": {
        "blockToolbar": [
            "paragraph", "heading1", "heading2", "heading3",
            "|",
            "bulletedList", "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": ["removeFormat", "|", "heading", "outdent", "indent", "|", "bold", "italic",
                    "link", "underline", "strikethrough",
                    "code", "subscript", "superscript", "highlight", "|", "codeBlock",
                    "sourceEditing", "insertImage",
                    "bulletedList", "numberedList", "todoList", "|", "blockQuote",
                    "|", "fontSize", "fontFamily", "fontColor", "fontBackgroundColor",
                    "mediaEmbed",
                    "insertTable", ],
        "image": {
            "toolbar": ["imageTextAlternative", "|", "imageStyle:alignLeft",
                        "imageStyle:alignRight", "imageStyle:alignCenter",
                        "imageStyle:side", "|"],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ]

        },
        "table": {
            "contentToolbar": ["tableColumn", "tableRow", "mergeTableCells",
                               "tableProperties", "tableCellProperties"],
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph", "title": "Paragraph",
                    "class": "ck-heading_paragraph"
                },
                {
                    "model": "heading1", "view": "h1", "title": "Heading 1",
                    "class": "ck-heading_heading1"
                },
                {
                    "model": "heading2", "view": "h2", "title": "Heading 2",
                    "class": "ck-heading_heading2"
                },
                {
                    "model": "heading3", "view": "h3", "title": "Heading 3",
                    "class": "ck-heading_heading3"
                }
            ]
        }
    },
    "list": {
        "properties": {
            "styles": "true",
            "startIndex": "true",
            "reversed": "true",
        }
    }
}

CKEDITOR_5_UPLOAD_PATH = "mediafiles/"

# Make sure CKEDITOR_5_UPLOAD_PATH is inside MEDIA_ROOT
CKEDITOR_5_MEDIA_PREFIX = f"{MEDIA_URL}{CKEDITOR_5_UPLOAD_PATH}"
