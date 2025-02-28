from django.contrib import admin
from django.contrib import messages
from django.forms import TextInput, Textarea
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from pages.models import Page
from pages.services.tasks import generate_content_task
from seo.admin import SEOInline


class PageForm(TranslatableModelForm):
    class Meta:
        model = Page
        fields = "__all__"
        widgets = {
            "title": TextInput(attrs={"style": "width: 100%;"}),
            "slug": TextInput(attrs={"style": "width: 100%;"}),
            "description": Textarea(attrs={"style": "width: 100%;"}),
        }


@admin.register(Page)
class PageAdmin(TranslatableAdmin):
    form = PageForm
    fields = ["title", "slug", "is_home", "status", "ai_additional_info", "content", "image", "publish"]
    list_display = ["title", "slug", "is_home", "publish", "status"]
    list_filter = ["is_home", "created", "publish"]
    list_editable = ["status"]
    inlines = [SEOInline]
    date_hierarchy = "publish"
    ordering = ["status", "-publish"]
    show_facets = admin.ShowFacets.ALWAYS
    actions = [
        "generate_content_for_pages",
        # "auto_translate"
    ]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("title",)}

    @admin.action(description="Generate content using AI")
    def generate_content_for_pages(self, request, queryset):
        """
        Generates content via together.ai for selected pages.
        Launches content generation through Celery for each page separately.
        """
        for page in queryset:
            generate_content_task.delay(page.id)

        messages.info(request, f"Started content generation for {queryset.count()} pages")

#     @admin.action(description="Translate into all languages")
#     def auto_translate(modeladmin, request, queryset):
#         """
#         Automatically translates selected pages into all languages specified in LANGUAGES.
#         Translates title, content, seo_title, seo_description.
#         """
#         languages = [lang[0] for lang in settings.LANGUAGES]
#
#         for page in queryset:
#             main_language = page.get_current_language()
#
#             for lang in languages:
#                 if lang == main_language:
#                     continue  # Skip the main language
#
#                 translation_service = TranslationService(page, lang)
#                 translations = translation_service.translate()
#
#                 # Translation of title and content for the page
#                 update_translated_field(page, lang, "title", translations)
#                 update_translated_field(page, lang, "content", translations)
#
#                 # Translation of SEO fields
#                 seo_fields = ["title", "description"]
#                 seo_object = SEO.objects.filter(object_id=page.id).first()
#                 if seo_object:
#                     for field in seo_fields:
#                         update_seo_field(seo_object, lang, field, translations)
#
#         messages.success(request, "Translation completed successfully!")
#
#
# def update_translated_field(page, lang, field, translations):
#     """
#     Updates the page field with the translation.
#     """
#     if translations.get(field):
#         with switch_language(page, lang):
#             setattr(page, field, translations[field])
#             page.save()
#
#
# def update_seo_field(seo_object, lang, field, translations):
#     """
#     Updates the SEO field for a SEO object with a translation.
#     """
#     if translations.get(f"seo_{field}"):
#         with switch_language(seo_object, lang):
#             setattr(seo_object, field, translations[f"seo_{field}"])
#             seo_object.save()
