from django import template
from django.urls import resolve, reverse, Resolver404
from django.utils.translation import activate
from parler.utils.context import switch_language

from site_service import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def change_lang_url(context, lang):
    path = context["request"].path
    try:
        url_parts = resolve(path)
    except Resolver404:
        return path

    obj = context.get("object")
    if obj and hasattr(obj, "get_absolute_url"):
        try:
            with switch_language(obj, lang):
                return obj.get_absolute_url()
        except AttributeError:
            pass

    # If the object does not exist or does not have a get_absolute_url, or an error occurred
    try:
        with activate(lang):
            return reverse(url_parts.view_name, kwargs=url_parts.kwargs)
    except Exception:
        return path  # Return the original path in case of any error


@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key, key)
    return key


@register.filter
def language_url(request, lang_code):
    """Generates a URL for the selected language, keeping the current path."""
    old_language = request.LANGUAGE_CODE
    try:
        activate(lang_code)
        url = request.build_absolute_uri()
    finally:
        activate(old_language)
    return url


@register.simple_tag
def get_parler_fallback_language():
    parler_languages = getattr(settings, 'PARLER_LANGUAGES', {})
    default_config = parler_languages.get('default', {})
    return default_config.get('fallback', settings.LANGUAGE_CODE)
