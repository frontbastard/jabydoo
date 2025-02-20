from django.urls import path

from .models import Page
from .views import PageDetailView

app_name = "pages"

urlpatterns = []

home_page = Page.objects.filter(is_home=True).first()

if home_page:
    urlpatterns.append(path("", PageDetailView.as_view(), {"slug": home_page.slug}, name="home"))

urlpatterns.append(path("<slug:slug>/", PageDetailView.as_view(), name="page_detail"))
