from django import template

from core.models import SiteOptions

register = template.Library()


@register.filter(name="sponsor_info")
def sponsor_info(value):
    options = SiteOptions.get_options()
    if "[sponsor_url]" in value:
        value = value.replace("[sponsor_url]", options.sponsor_url)
    if "[sponsor_name]" in value:
        value = value.replace("[sponsor_name]", options.sponsor_name)
    if "[sponsor_link]" in value:
        value = value.replace("[sponsor_link]", f"<a href='{options.sponsor_url}'>{options.sponsor_name}</a>")
    return value
