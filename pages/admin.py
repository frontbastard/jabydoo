from django.contrib import admin
from django.contrib import messages
from parler.admin import TranslatableAdmin

from pages.models import Page
from seo.admin import SEOInline


@admin.register(Page)
class PageAdmin(TranslatableAdmin):
    fields = ["title", "slug", "is_home", "status", "auto_generate_content", "ai_additional_info", "content", "image",
              "publish"]
    list_display = ["title", "slug", "is_home", "publish", "status"]
    list_filter = ["is_home", "created", "publish"]
    list_editable = ["status"]
    inlines = [SEOInline]
    date_hierarchy = "publish"
    ordering = ["status", "-publish"]
    show_facets = admin.ShowFacets.ALWAYS
    actions = ["generate_content_for_selected"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("title",)}

    @admin.action(description="Generate content for selected pages")
    def generate_content_for_selected(self, request, queryset):
        for page in queryset:
            page.auto_generate_content = True
            page.generate_content_and_seo(request)
        self.message_user(request, "Content successfully generated", messages.SUCCESS)
