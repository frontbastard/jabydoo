import os
from pathlib import Path

from decouple import config
from django.utils.translation import gettext_lazy as _

from core.enums import Environment

SITE_ID = 1
BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENVIRONMENT = config("ENVIRONMENT", default=Environment.PROD.value)
DEBUG = config("DJANGO_DEBUG", "True") == "True"

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

    "core",
    "pages",
    "seo",
    "menu",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "site_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.language_flag_map",
                "core.context_processors.site_options",
                "core.context_processors.environment_processor",
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

# International settings
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", _("English")),
    ("fr", _("French")),
]
LANGUAGE_FLAG_MAP = {
    "en": "gb",
    "fr": "fr",
}

LOCALE_PATHS = [BASE_DIR / "locale"]

PARLER_LANGUAGES = {
    1: (
        {"code": "en"},
        {"code": "fr"},
    ),
    "default": {
        "fallback": "en",
        "hide_untranslated": False,
    }
}

TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

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

CKEDITOR_5_UPLOAD_PATH = "media/"

# Make sure CKEDITOR_5_UPLOAD_PATH is inside MEDIA_ROOT
CKEDITOR_5_MEDIA_PREFIX = f"{MEDIA_URL}{CKEDITOR_5_UPLOAD_PATH}"
