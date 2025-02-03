from decouple import config
from easy_thumbnails.signals import thumbnail_created
from django.dispatch import receiver

from core.utils import add_watermark


@receiver(thumbnail_created)
def thumbnail_callback(sender, **kwargs):
    add_watermark(sender.path, config("SITE_DOMAIN"))
