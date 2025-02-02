from django import template
from django.contrib.contenttypes.models import ContentType
from seo.models import SEO

register = template.Library()


@register.simple_tag
def get_seo(obj):
    if not hasattr(obj, "_meta"):
        return None
    try:
        content_type = ContentType.objects.get_for_model(obj)
        return SEO.objects.get(content_type=content_type, object_id=obj.id)
    except SEO.DoesNotExist:
        return None
