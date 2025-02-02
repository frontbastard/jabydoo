from django import template

register = template.Library()

from django.conf import settings
from django.urls import resolve, reverse
from django.utils.translation import get_language


@register.simple_tag(takes_context=True)
def change_lang_url(context, lang):
    request = context["request"]
    current_lang = get_language()
    resolved_url = resolve(request.path_info)
    url_name = resolved_url.url_name
    args = resolved_url.args
    kwargs = resolved_url.kwargs

    # Add the namespace, if it exists
    if resolved_url.namespace:
        url_name = f"{resolved_url.namespace}:{url_name}"

    # Generate a new URL
    new_url = reverse(url_name, args=args, kwargs=kwargs)

    # Remove the current language prefix, if any
    if current_lang != settings.LANGUAGE_CODE:
        new_url = new_url.replace(f"/{current_lang}", "", 1)

    # Add a new language prefix only if it is not the default language
    if lang != settings.LANGUAGE_CODE:
        return f"/{lang}{new_url}"
    else:
        return new_url
