from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.utils.text import slugify

from menu.models import MenuItem, Menu
from pages.models import Page


@receiver(post_migrate)
def create_default_menus(sender, **kwargs):
    if sender.name == "menu":
        Menu.objects.get_or_create(name="Main Menu")
        Menu.objects.get_or_create(name="Footer Menu")


@receiver(post_save, sender=MenuItem)
def create_page_for_menu(sender, instance, created, **kwargs):
    """Automatically create a Page when a new MenuItem is created."""
    if created and instance.parent is None:  # Only for root elements
        slug = slugify(instance.name)

        # If the URL is "#" (hash), skip page creation
        if instance.url == "/#":
            return

        # Check if a page with this slug already exists
        if not Page.objects.filter(slug=slug).exists():
            Page.objects.create(
                title=instance.name,
                slug=slug,
                status=Page.Status.PUBLISHED
            )
