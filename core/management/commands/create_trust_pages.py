from django.core.management.base import BaseCommand
from django.utils.text import slugify
from pages.models import Page

TRUST_PAGES = [
    {"title": "Privacy Policy"},
    {"title": "Terms of Service"},
    {"title": "Contact Us"},
    {"title": "About Us"},
    {"title": "FAQ"},
    {"title": "Cookie Policy"},
]


class Command(BaseCommand):
    help = "Creates default trust pages if they do not exist."

    def handle(self, *args, **kwargs):
        for page_data in TRUST_PAGES:
            slug = slugify(page_data["title"])
            page, created = Page.objects.get_or_create(slug=slug)

            if not page.has_translation("en"):
                page.set_current_language("en")
                page.title = page_data["title"]
                page.save()

            self.stdout.write(self.style.SUCCESS(
                f'Page "{page.safe_translation_getter("title", any_language=True) or page.slug}" exists.'))
