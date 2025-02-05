from django import template
from django.conf import settings

register = template.Library()


@register.filter(name="sponsor_info")
def sponsor_info(value):
    if '[sponsor_url]' in value:
        value = value.replace('[sponsor_url]', settings.SPONSOR_URL)
    if '[sponsor_name]' in value:
        value = value.replace('[sponsor_name]', settings.SPONSOR_NAME)
    if '[sponsor_link]' in value:
        value = value.replace('[sponsor_link]', f"<a href='{settings.SPONSOR_URL}'>{settings.SPONSOR_NAME}</a>")
    return value
