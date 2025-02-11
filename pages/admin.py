from django.contrib import admin
from parler.admin import TranslatableAdmin

from pages.models import Page
from seo.admin import SEOInline


@admin.register(Page)
class PageAdmin(TranslatableAdmin):
    list_display = ["title", "slug", "is_home", "publish", "status"]
    list_filter = ["is_home", "created", "publish"]
    list_editable = ["is_home", "status"]
    inlines = [SEOInline]
    date_hierarchy = "publish"
    ordering = ["status", "-publish"]
    show_facets = admin.ShowFacets.ALWAYS

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("title",)}
