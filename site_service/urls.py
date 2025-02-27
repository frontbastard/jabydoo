"""
URL configuration for site_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView

from core.enums import Environment
from core.sitemaps import PageSitemap, HomepageSitemap

sitemaps = {
    "home": HomepageSitemap,
    "pages": PageSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path(
        "robots.txt", TemplateView.as_view(
            template_name="robots.txt", content_type="text/plain"
        )
    ),
    path(
        "sitemap.xml", sitemap, {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap"
    ),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]

urlpatterns += i18n_patterns(
    path("", include("pages.urls", namespace="pages")),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

if settings.ENVIRONMENT == Environment.DEV.value:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

