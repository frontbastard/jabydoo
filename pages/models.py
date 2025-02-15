import json

import requests
from decouple import config
from django.contrib import messages
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation.trans_null import get_language
from django_ckeditor_5.fields import CKEditor5Field
from filer.fields.image import FilerImageField
from parler.managers import TranslatableQuerySet
from parler.models import TranslatableModel, TranslatedFields
from together import Together

from core.models import SiteOptions


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
            self.generate_content(request=request)

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

    def generate_content(self, request=None):
        """
        Generates content via the Together API.
        """
        sponsor_name = getattr(SiteOptions.get_options(), "sponsor_name", "").strip()

        if not sponsor_name:
            error_message = "Error: SiteOptions.sponsor_name haven't been set!"
            if request:
                messages.error(request, error_message)
            self.content = error_message
            return

        if len(self.content) > 20:
            return

        language = self.get_current_language()

        title = self.title
        additional_info = self.ai_additional_info or ""
        site_type = getattr(SiteOptions.get_options(), "site_type", "")

        prompt = (
            f"Згенеруй змістовний та унікальний SEO контент для статті '{title}' для сайту {sponsor_name}. "
            f"Врахуй, що мова сайту – {language}. Тип сайту — {site_type}"
            f"Не використовуй заповнювачі потипу [Insert Date]. Не використовуй ніяких посилань в тексті."
            f"Або використовуй фейкові дані наближені до реальних або не використовуй взагалі."
            f"Генеруй контент в html для візуального редактора в джанго CKEDITOR 5."
            f"На початку не потрібно додавати h1 заголовок, він вже є в шаблоні."
            f"Подальші інструкції мають приорітет перед попередніми: {additional_info}"
        )

        client = Together(api_key=getattr(SiteOptions.get_options(), "ai_secret_key", ""))

        try:
            response = client.chat.completions.create(
                model=getattr(SiteOptions.get_options(), "ai_model", ""),
                messages=[{"role": "user", "content": prompt}]
            )
            generated_text = response.choices[0].message.content.strip()

            self.content = generated_text
        except Exception as e:

            self.content = f"Generation error: {e}"
