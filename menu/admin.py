from mptt.forms import MPTTAdminForm
from parler.admin import TranslatableModelForm


class MenuItemAdminForm(MPTTAdminForm, TranslatableModelForm):
    pass


from django.contrib import admin
from parler.admin import TranslatableAdmin
from mptt.admin import DraggableMPTTAdmin
from .models import MenuItem


class MenuItemAdmin(TranslatableAdmin, DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_title', 'url', 'order']
    list_display_links = ['indented_title']
    list_editable = ['order']
    mptt_level_indent = 20


admin.site.register(MenuItem, MenuItemAdmin)
