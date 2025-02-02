from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home_page, name="home"),
    path("<slug:slug>/", views.other_page, name="page"),
]
