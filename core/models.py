from django.db import models
from filer.fields.image import FilerImageField
from filer.models import Folder


class SiteOptions(models.Model):
    sponsor_name = models.CharField(max_length=255)
    sponsor_url = models.URLField(max_length=255)
    hide_sponsor_url = models.BooleanField(default=False, help_text="Hide sponsor url from search engines")
    site_type = models.CharField(max_length=255, null=True, blank=True)
    sponsor_logo = FilerImageField(
        related_name="sponsor_logo",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ai_secret_key = models.CharField(max_length=255, null=True, blank=True)
    ai_model = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Model used for text generation. For example: meta-llama/Llama-3.3-70B-Instruct-Turbo"
    )

    def __str__(self):
        return "Options"

    def save(self, *args, **kwargs):
        if SiteOptions.objects.exists() and not self.pk:
            raise ValueError("There is already a SiteOptions record. Delete the old one before creating a new one.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Options"
        verbose_name_plural = "Options"

    @staticmethod
    def get_options():
        return SiteOptions.objects.first()
