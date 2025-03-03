from django.contrib import admin
from django.forms import TextInput
from mptt.admin import DraggableMPTTAdmin
from mptt.forms import MPTTAdminForm
from parler.admin import TranslatableAdmin
from parler.admin import TranslatableModelForm

from .models import MenuItem, Menu


class MenuItemAdminForm(MPTTAdminForm, TranslatableModelForm):
    pass


class MenuItemForm(TranslatableModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"
        widgets = {
            "name": TextInput(attrs={"style": "width: 100%;"}),
            "url": TextInput(attrs={"style": "width: 100%;"}),
        }


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    form = MenuItemForm
    extra = 0
    fields = ["name", "url", "parent", "order"]
    widgets = {
        "name": TextInput(attrs={"style": "width: 100%;"}),
        "url": TextInput(attrs={"style": "width: 100%;"}),
    }
    mptt_level_indent = 20

    def get_prepopulated_fields(self, request, obj=None):
        return {"url": ("name",)}


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MenuItem)
class MenuItemAdmin(TranslatableAdmin, DraggableMPTTAdmin):
    form = MenuItemForm
    fields = ["name", "url", "parent", "order"]
    list_display = ["tree_actions", "indented_title", "url", "order"]
    list_display_links = ["indented_title"]
    list_editable = ["order"]
    mptt_level_indent = 20

    def get_prepopulated_fields(self, request, obj=None):
        return {"url": ("name",)}
