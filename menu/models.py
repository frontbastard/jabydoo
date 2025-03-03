from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields

from menu.managers import MenuItemManager


def get_default_menu():
    menu, created = Menu.objects.get_or_create(name="Main Menu")
    return menu.id


class Menu(models.Model):
    """Model to define different menus (e.g., Main, Footer, Sidebar)."""
    name = models.CharField(max_length=100, unique=True)

    def delete(self, *args, **kwargs):
        raise ValueError("Deleting menus is not allowed.")

    def __str__(self):
        return self.name


class MenuItem(MPTTModel, TranslatableModel):
    """Menu item that belongs to a specific Menu."""
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="items",
        default=get_default_menu
    )
    url = models.CharField(max_length=200)
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children",
        on_delete=models.CASCADE
    )
    order = models.IntegerField(default=0)

    objects = MenuItemManager()

    class MPTTMeta:
        order_insertion_by = ["order"]

    def __str__(self):
        return self.safe_translation_getter(
            "name", any_language=True
        ) or "Unnamed Menu Item"

    def save(self, *args, **kwargs):
        if self.url and not self.url.startswith("/"):
            self.url = "/" + self.url.lstrip("/")
        super().save(*args, **kwargs)
