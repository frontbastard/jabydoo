from django import template
from django.db.models import Prefetch
from django.utils.translation import get_language

from menu.models import MenuItem, Menu

register = template.Library()

@register.simple_tag
def get_menu(menu_name):
    """Returns a menu for use in any template."""
    language_code = get_language()
    return MenuItem.objects.get_menu(menu_name=menu_name, language_code=language_code)
