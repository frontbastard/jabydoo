from django.contrib.contenttypes.admin import GenericStackedInline
from .models import SEO


class SEOInline(GenericStackedInline):
    model = SEO
    extra = 1
    max_num = 1
