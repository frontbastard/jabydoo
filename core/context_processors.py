from django.urls import resolve

from pages.models import Page


def all_pages(request):
    return {
        "all_pages": Page.objects.filter(
            is_home=False,
            status=Page.Status.PUBLISHED
        )
    }


def current_url_name(request):
    resolved_url = resolve(request.path_info)
    return {"current_url_name": resolved_url.url_name}
