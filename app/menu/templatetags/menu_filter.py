from django import template
from django.conf import settings

register = template.Library()


@register.filter
def add_language_prefix(url, language_code):
    default_language = settings.LANGUAGE_CODE

    if language_code != default_language:
        if not url.startswith("/"):
            return url
        return f"/{language_code}{url}"

    return url
