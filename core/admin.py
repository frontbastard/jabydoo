from django.contrib import admin
from .models import SiteOptions, Partners


@admin.register(SiteOptions)
class SiteOptionsAdmin(admin.ModelAdmin):
    list_display = ["sponsor_name", "sponsor_url", "sponsor_logo"]


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ["name", "url"]
