from django.conf import settings
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

LANGUAGES = [lang[0] for lang in settings.LANGUAGES]


class Command(BaseCommand):
    help = "Creates default trust pages if they do not exist."

    def handle(self, *args, **kwargs):
        for page_data in TRUST_PAGES:
            slug = slugify(page_data["title"])

            page, created = Page.objects.get_or_create(slug=slug)

            if created:
                self.stdout.write(self.style.SUCCESS(f'Page "{page.title}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Page "{page.title}" already exists.'))
