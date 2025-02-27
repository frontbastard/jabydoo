from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from menu.models import MenuItem
from pages.models import Page


@receiver(post_save, sender=MenuItem)
def create_page_for_menu(sender, instance, created, **kwargs):
    """Automatically create a Page when a new MenuItem is created."""
    if created and instance.parent is None:  # Тільки для кореневих елементів
        slug = slugify(instance.name)

        # Перевіряємо, чи вже існує сторінка з таким slug
        if not Page.objects.filter(slug=slug).exists():
            Page.objects.create(
                title=instance.name,
                slug=slug,
                status=Page.Status.PUBLISHED
            )
