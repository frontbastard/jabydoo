from django.db import models
from parler.managers import TranslatableManager
from parler.models import TranslatableModel, TranslatedFields
from mptt.models import MPTTModel, TreeForeignKey
from menu.managers import MenuItemManager


class MenuItem(MPTTModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
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
