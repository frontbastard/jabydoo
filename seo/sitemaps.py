from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from django.contrib.sitemaps import Sitemap

from pages.models import Page


class PageSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Page.objects.filter(status=Page.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated
