from django import template

register = template.Library()


@register.simple_tag
def page_json_ld(page):
    return page.get_json_ld()
