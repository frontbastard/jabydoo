from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class SEOModel(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True


class SEO(SEOModel):
    class Meta:
        unique_together = ["content_type", "object_id"]
