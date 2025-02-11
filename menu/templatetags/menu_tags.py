from django import template
from django.utils.translation import get_language

from menu.models import MenuItem

register = template.Library()


@register.inclusion_tag("menu/menu.html")
def render_menu():
    language_code = get_language()
    return {
        "menu_items": MenuItem.objects.filter(parent=None).order_by("order"),
        "language_code": language_code
    }
