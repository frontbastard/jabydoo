from django import template
from django.urls import resolve, reverse
from django.utils.translation import activate, get_language
from parler.utils.context import switch_language

from site_service import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def change_lang_url(context, lang):
    request = context["request"]
    path = request.path
    url_parts = resolve(path)

    # Check if the current page is the home page
    is_home = path == "/" or path == f"/{get_language()}/"

    if is_home:
        # If this is the main page, just change the language prefix
        if lang == settings.LANGUAGE_CODE:
            return "/"
        else:
            return f"/{lang}/"
    else:
        # For other pages, use the previous logic
        obj = context.get("object")
        if obj and hasattr(obj, "get_absolute_url"):
            with switch_language(obj, lang):
                return obj.get_absolute_url()
        else:
            with activate(lang):
                return reverse(url_parts.view_name, kwargs=url_parts.kwargs)
