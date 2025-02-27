from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.conf import settings
from pages.models import Page

# Додаємо підтримку різних мов для кожної сторінки
TRUST_PAGES = {
    "en": [
        {"title": "Privacy Policy", "slug": "privacy-policy"},
        {"title": "Terms of Service", "slug": "terms-of-service"},
        {"title": "Contact Us", "slug": "contact-us"},
        {"title": "About Us", "slug": "about-us"},
        {"title": "FAQ", "slug": "faq"},
        {"title": "Cookie Policy", "slug": "cookie-policy"},
    ],
    "de": [
        {"title": "Datenschutzrichtlinie", "slug": "privacy-policy"},
        {"title": "Nutzungsbedingungen", "slug": "terms-of-service"},
        {"title": "Kontakt", "slug": "contact-us"},
        {"title": "Über uns", "slug": "about-us"},
        {"title": "FAQ", "slug": "faq"},
        {"title": "Cookie-Richtlinie", "slug": "cookie-policy"},
    ],
}


class Command(BaseCommand):
    help = "Creates default trust pages in the active LANGUAGE_CODE if they do not exist."

    def handle(self, *args, **kwargs):
        # Get the current language from Django settings
        lang_code = settings.LANGUAGE_CODE
        pages = TRUST_PAGES.get(lang_code, TRUST_PAGES["en"])  # If there is no language, we use English

        for page_data in pages:
            slug = page_data["slug"]
            page, created = Page.objects.get_or_create(slug=slug)

            # Set the correct language before saving
            if not page.has_translation(lang_code):
                page.set_current_language(lang_code)
                page.title = page_data["title"]
                page.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Page "{page.title}" was created in {lang_code}.'))
            else:
                self.stdout.write(self.style.WARNING(f'Page "{page.title}" already exists in {lang_code}.'))
