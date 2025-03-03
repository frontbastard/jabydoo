from django import template
from django.db.models import Prefetch
from django.utils.translation import get_language

from menu.models import MenuItem, Menu

register = template.Library()


@register.inclusion_tag("includes/menu/main_menu.html")
def render_main_menu():
    language_code = get_language()
    menu = Menu.objects.get(name="Main Menu")
    menu_items = MenuItem.objects.filter(menu=menu).order_by("order")
    return {
        "menu_items": menu_items,
        "language_code": language_code
    }


@register.inclusion_tag("includes/menu/footer_menu.html")
def render_footer_menu():
    language_code = get_language()
    menu = Menu.objects.get(name="Footer Menu")
    menu_items = MenuItem.objects.filter(menu=menu).order_by("order")
    return {
        "menu_items": menu_items,
        "language_code": language_code
    }
