from django.db import models
from django.forms import Textarea, TextInput
from mptt.forms import MPTTAdminForm
from parler.admin import TranslatableModelForm


class MenuItemAdminForm(MPTTAdminForm, TranslatableModelForm):
    pass


from django.contrib import admin
from parler.admin import TranslatableAdmin
from mptt.admin import DraggableMPTTAdmin
from .models import MenuItem


class MenuItemForm(TranslatableModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"
        widgets = {
            "name": TextInput(attrs={"style": "width: 100%;"}),
            "url": TextInput(attrs={"style": "width: 100%;"}),
        }


class MenuItemAdmin(TranslatableAdmin, DraggableMPTTAdmin):
    form = MenuItemForm
    fields = ["name", "url", "parent", "order"]
    list_display = ["tree_actions", "indented_title", "url", "order"]
    list_display_links = ["indented_title"]
    list_editable = ["order"]
    mptt_level_indent = 20

    def get_prepopulated_fields(self, request, obj=None):
        return {"url": ("name",)}


admin.site.register(MenuItem, MenuItemAdmin)
