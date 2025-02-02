from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.urls import reverse


class PageManager(models.Manager):
    def get_home_page(self):
        return self.filter(is_home=True).first()


class PuglishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Page.Status.PUBLISHED)
        )


class Page(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    content = RichTextField()
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
        return reverse("pages:page", kwargs={"slug": self.slug})
