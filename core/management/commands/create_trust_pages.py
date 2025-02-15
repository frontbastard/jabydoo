from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.conf import settings
from pages.models import Page
from django.utils.translation import activate

TRUST_PAGES = [
    {"title": "Privacy Policy", "content": "Privacy Policy"},
    {"title": "Terms of Service", "content": "Terms of Service"},
    {"title": "Contact Us", "content": "Contact Us"},
    {"title": "About Us", "content": "About Us"},
    {"title": "FAQ", "content": "FAQ"},
    {"title": "Cookie Policy", "content": "Cookie Policy"},
]

LANGUAGES = [lang[0] for lang in settings.LANGUAGES]


class Command(BaseCommand):
    help = "Creates default trust pages with multilingual support if they do not exist."

    def handle(self, *args, **kwargs):
        for page_data in TRUST_PAGES:
            slug = slugify(page_data["title"])
            page, created = Page.objects.get_or_create(slug=slug)

            for lang in LANGUAGES:
                activate(lang)
                page.set_current_language(lang)
                page.title = page_data["title"]
                page.content = page_data["content"]
                page.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Page "{page.title}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Page "{page.title}" already exists.'))
