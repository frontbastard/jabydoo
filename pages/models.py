import json

from decouple import config
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from filer.fields.image import FilerImageField
from parler.managers import TranslatableQuerySet
from parler.models import TranslatableModel, TranslatedFields

from core.models import SiteOptions
from core.services.content_generation import ContentGenerationService
from core.services.seo_generation import SEOGenerationService
from seo.models import SEO


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
        default=Status.PUBLISHED
    )
    image = FilerImageField(
        null=True,
        blank=True,
        related_name="product_image",
        on_delete=models.SET_NULL
    )
    auto_generate_content = models.BooleanField(
        default=False,
        help_text="If active, new content will be generated on save, but only if the content is empty"
    )
    ai_additional_info = models.TextField(
        blank=True,
        help_text="In addition to the main request, these additional instructions will be used (they are in priority)"
    )

    objects = PageManager()

    def save(self, *args, **kwargs):
        request = kwargs.pop("request", None)

        if self.auto_generate_content:
            service = ContentGenerationService(self, request)
            service.generate()

        if self.auto_generate_content:
            seo, created = SEO.objects.get_or_create(
                content_type=ContentType.objects.get_for_model(Page),
                object_id=self.pk,
                defaults={"title": "", "description": ""}
            )
            seo_service = SEOGenerationService(self, request)
            seo_data = seo_service.generate()

            if isinstance(seo_data, dict):
                seo.title = seo_data["title"]
                seo.description = seo_data["description"]
                seo.save()

        if self.is_home:
            Page.objects.exclude(pk=self.pk).update(is_home=False)

        super().save(*args, **kwargs)

        if self.auto_generate_content:
            self.auto_generate_content = False
            self.save(update_fields=["auto_generate_content"])

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
