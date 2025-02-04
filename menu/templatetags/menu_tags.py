from django import template
from menu.models import MenuItem

register = template.Library()


@register.inclusion_tag("menu/menu.html")
def render_menu():
    return {"menu_items": MenuItem.objects.filter(parent=None).order_by("order")}
