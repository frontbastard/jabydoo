from django.contrib.contenttypes.admin import GenericStackedInline
from parler.admin import TranslatableStackedInline

from .models import SEO


class SEOInline(GenericStackedInline, TranslatableStackedInline):
    model = SEO
    extra = 1
    max_num = 1
    fields = ["title", "description", "keywords"]
