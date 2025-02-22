import json

from decouple import config
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from filer.fields.image import FilerImageField
from parler.managers import TranslatableQuerySet
from parler.models import TranslatableModel, TranslatedFields

from seo.models import SEO


class PageQuerySet(TranslatableQuerySet):
    def published(self):
        """Filters only published pages."""
        return self.filter(status=Page.Status.PUBLISHED)

    def home_page(self):
        """Gets the home page if it is published."""
        return self.published().filter(is_home=True).first()


class PageManager(models.Manager):
    def get_queryset(self):
        return PageQuerySet(self.model, using=self._db)

    def get_home_page(self):
        return self.get_queryset().home_page()

    def get_published(self):
        return self.get_queryset().published()


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
        default=Status.PUBLISHED
    )
    image = FilerImageField(
        null=True,
        blank=True,
        related_name="product_image",
        on_delete=models.SET_NULL
    )
    ai_additional_info = models.TextField(
        null=True,
        blank=True,
        help_text="Additional AI generation instructions"
    )
    seo = GenericRelation(SEO)

    objects = PageManager()

    class Meta:
        ordering = ["-publish"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_home:
            Page.objects.exclude(pk=self.pk).update(is_home=False)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("pages:home") if self.is_home else reverse(
            "pages:page_detail",
            kwargs={"slug": self.slug}
        )

    def get_json_ld(self):
        """Generates structured JSON-LD data for SEO"""
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

        return mark_safe(f"<script type='application/ld+json'>{json.dumps(data, ensure_ascii=False)}</script>")
