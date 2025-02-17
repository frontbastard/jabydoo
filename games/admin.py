from django.contrib import admin

from games.models import Game


@admin.register(Game)
class SiteOptionsAdmin(admin.ModelAdmin):
    list_display = ["title", "image", "order"]
    list_editable = ["order"]
    ordering = ["id"]
