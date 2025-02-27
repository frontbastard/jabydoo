from django.contrib.contenttypes.admin import GenericStackedInline
from django.db import models
from django.forms import Textarea, TextInput
from parler.admin import TranslatableStackedInline
from parler.forms import TranslatableModelForm

from .models import SEO


class SEOForm(TranslatableModelForm):
    class Meta:
        model = SEO
        fields = "__all__"
        widgets = {
            "title": TextInput(attrs={"style": "width: 100%;"}),
            "description": Textarea(attrs={"style": "width: 100%;"}),
        }


class SEOInline(GenericStackedInline, TranslatableStackedInline):
    form = SEOForm
    model = SEO
    extra = 1
    max_num = 1
    fields = ["title", "description"]
