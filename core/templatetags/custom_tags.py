from django import template
from django.urls import resolve, reverse, Resolver404
from django.utils.translation import activate
from parler.utils.context import switch_language

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
