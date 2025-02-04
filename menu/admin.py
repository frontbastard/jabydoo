from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from mptt.forms import MPTTAdminForm
from parler.admin import TranslatableAdmin, TranslatableModelForm

from .models import MenuItem


class MenuItemAdminForm(MPTTAdminForm, TranslatableModelForm):
    pass


class MenuItemAdmin(TranslatableAdmin, MPTTModelAdmin):
    form = MenuItemAdminForm

    def get_prepopulated_fields(self, request, obj=None):
        return {"url": ("name",)}  # needed for translated fields


admin.site.register(MenuItem, MenuItemAdmin)
