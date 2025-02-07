import json

from decouple import config
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from filer.fields.image import FilerImageField
from parler.managers import TranslatableQuerySet
from parler.models import TranslatableModel, TranslatedFields


class PageQuerySet(TranslatableQuerySet):
    pass


class PageManager(models.Manager):
    def get_home_page(self):
        return self.filter(is_home=True).first()

    def get_queryset(self):
        return PageQuerySet(self.model, using=self._db)


class PuglishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Page.Status.PUBLISHED)
        )


class Page(TranslatableModel):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    translations = TranslatedFields(
        title=models.CharField(max_length=250),
        content=CKEditor5Field("Content", config_name="extends"),
    )
    slug = models.SlugField(max_length=250, unique=True)
    is_home = models.BooleanField(default=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    image = FilerImageField(
        null=True,
        blank=True,
        related_name="product_image",
        on_delete=models.SET_NULL
    )

    objects = PageManager()

    def save(self, *args, **kwargs):
        if self.is_home:
            Page.objects.exclude(pk=self.pk).update(is_home=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-publish"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.is_home:
            return reverse("pages:home")
        return reverse("pages:page", kwargs={"slug": self.slug})

    def get_json_ld(self):
        data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": self.title,
            "description": self.content[:150],
            "datePublished": self.publish.isoformat(),
            "dateModified": self.updated.isoformat(),
            "url": f"https://{config('SITE_DOMAIN', default='site-domain.com')}{self.get_absolute_url()}",
        }

        if self.image:
            data["image"] = f"https://{config('SITE_DOMAIN', default='site-domain.com')}{self.image.url}"

        json_ld = json.dumps(data, ensure_ascii=False)
        return mark_safe(
            f"<script type='application/ld+json'>{json_ld}</script>"
        )
