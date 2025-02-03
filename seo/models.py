from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from parler.models import TranslatableModel, TranslatedFields


class SEO(TranslatableModel):

    translations = TranslatedFields(
        title=models.CharField(max_length=200, blank=True),
        description=models.TextField(blank=True),
        keywords=models.CharField(max_length=500, blank=True),
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        unique_together = ["content_type", "object_id"]

    def __str__(self):
        return f"SEO for {self.content_type.model} (ID: {self.object_id}): {self.title[:50]}"
