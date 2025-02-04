from django import template
from filer.models import Image

register = template.Library()


@register.simple_tag
def get_filer_image(image_name):
    try:
        return Image.objects.get(name=image_name)
    except Image.DoesNotExist:
        return None
