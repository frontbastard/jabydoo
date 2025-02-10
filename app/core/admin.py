from django.contrib import admin
from .models import SiteOptions


@admin.register(SiteOptions)
class SiteOptionsAdmin(admin.ModelAdmin):
    list_display = ("sponsor_name", "sponsor_url", "sponsor_logo")
