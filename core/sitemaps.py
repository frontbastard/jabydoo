from django.contrib.sitemaps import Sitemap

from pages.models import Page


class HomepageSitemap(Sitemap):
    changefreq = "daily"
    priority = 1
    i18n = True

    def items(self):
        return Page.objects.filter(status=Page.Status.PUBLISHED, is_home=True)

    def lastmod(self, obj):
        return obj.updated


class PageSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    i18n = True

    def items(self):
        return Page.objects.filter(status=Page.Status.PUBLISHED, is_home=False)

    def lastmod(self, obj):
        return obj.updated
