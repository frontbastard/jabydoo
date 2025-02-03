from django import template
from django.urls import resolve, reverse
from django.utils.translation import activate
from parler.utils.context import switch_language

register = template.Library()


@register.simple_tag(takes_context=True)
def change_lang_url(context, lang):
    path = context["request"].path
    url_parts = resolve(path)

    obj = context.get("object")
    if obj and hasattr(obj, "get_absolute_url"):
        with switch_language(obj, lang):
            return obj.get_absolute_url()
    else:
        with activate(lang):
            return reverse(url_parts.view_name, kwargs=url_parts.kwargs)
