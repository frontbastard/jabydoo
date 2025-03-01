from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.forms import TextInput, Textarea
from django.http import HttpResponse, JsonResponse
from django.utils.html import format_html
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from core.models import SiteOptions
from core.services.ai_content_service import AIContentService, TogetherAIClient, ContentGenerationService, FileService
from seo.admin import SEOInline
from .models import Page


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
        if not request.user.is_superuser:
            raise PermissionDenied

        options = SiteOptions.get_options()
        ai_client = TogetherAIClient(api_key=options.ai_secret_key)
        content_service = ContentGenerationService(ai_client, options)
        file_service = FileService()
        ai_content_service = AIContentService(ai_client, content_service, file_service)

        results = {"success": [], "failed": [], "skipped": []}

        for page in queryset:
            result = ai_content_service.generate_content_for_page(page)
            if result["status"] == "success":
                results["success"].append(page)
            elif result["status"] == "failed":
                results["failed"].append(page)
            else:
                results["skipped"].append(page)

        success_count = len(results["success"])
        failed_count = len(results["failed"])
        skipped_count = len(results["skipped"])

        message = format_html(
            "Content generated for {} pages.<br>"
            "Failed for {} pages.<br>"
            "Skipped {} pages.",
            success_count, failed_count, skipped_count
        )

        self.message_user(request, message)

        # return JsonResponse({
        #     "message": message,
        #     "success": success_count,
        #     "failed": failed_count,
        #     "skipped": skipped_count
        # })

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
