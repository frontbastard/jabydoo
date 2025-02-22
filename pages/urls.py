from django.urls import path

from .views import PageDetailView

app_name = "pages"

urlpatterns = [
    path("", PageDetailView.as_view(), name="home"),
    path("<slug:slug>/", PageDetailView.as_view(), name="page_detail"),
]
