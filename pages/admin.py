from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from parler.admin import TranslatableAdmin
from parler.utils.context import switch_language

from core.services.content_translation import TranslationService
from pages.models import Page
from seo.admin import SEOInline
from seo.models import SEO


@admin.register(Page)
class PageAdmin(TranslatableAdmin):
    fields = ["title", "slug", "is_home", "status", "auto_generate_content", "ai_additional_info", "content", "image",
              "publish"]
    list_display = ["title", "slug", "is_home", "publish", "status", "language_column"]
    list_filter = ["is_home", "created", "publish"]
    list_editable = ["status"]
    inlines = [SEOInline]
    date_hierarchy = "publish"
    ordering = ["status", "-publish"]
    show_facets = admin.ShowFacets.ALWAYS
    actions = ["generate_content_for_selected", "auto_translate"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("title",)}

    def language_column(self, obj):
        return ", ".join(obj.get_available_languages())

    language_column.short_description = "Доступні мови"

    @admin.action(description="Generate content for selected pages")
    def generate_content_for_selected(self, request, queryset):
        for page in queryset:
            page.auto_generate_content = True
            page.generate_content_and_seo(request)
        self.message_user(request, "Content successfully generated", messages.SUCCESS)

    @admin.action(description="Translate into all languages")
    def auto_translate(modeladmin, request, queryset):
        """
        Automatically translates selected pages into all languages specified in LANGUAGES.
        Translates title, content, seo_title, seo_description.
        """
        languages = [lang[0] for lang in settings.LANGUAGES]

        for page in queryset:
            main_language = page.get_current_language()

            for lang in languages:
                if lang == main_language:
                    continue  # Skip the main language

                translation_service = TranslationService(page, lang)
                translations = translation_service.translate()

                # Translation of title and content for the page
                update_translated_field(page, lang, 'title', translations)
                update_translated_field(page, lang, 'content', translations)

                # Translation of SEO fields
                seo_fields = ['title', 'description', 'keywords']
                seo_object = SEO.objects.filter(object_id=page.id).first()
                if seo_object:
                    for field in seo_fields:
                        update_seo_field(seo_object, lang, field, translations)

        messages.success(request, "Translation completed successfully!")


def update_translated_field(page, lang, field, translations):
    """
    Updates the page field with the translation.
    """
    if translations.get(field):
        with switch_language(page, lang):
            setattr(page, field, translations[field])
            page.save()


def update_seo_field(seo_object, lang, field, translations):
    """
    Updates the SEO field for an SEO object with a translation.
    """
    if translations.get(f"seo_{field}"):
        with switch_language(seo_object, lang):
            setattr(seo_object, field, translations[f"seo_{field}"])
            seo_object.save()
