from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Page


def home_page(request):
    home = Page.objects.filter(
        is_home=True, status=Page.Status.PUBLISHED
    ).order_by("-is_home").first()

    if not home:
        home = Page.objects.filter(status=Page.Status.PUBLISHED).first()

    if not home:
        return render(request, "/pages/404.html", status=404)

    return render(
        request,
        "pages/home.html",
        {"object": home}
    )


def other_page(request, slug):
    language = request.LANGUAGE_CODE
    home = get_object_or_404(
        Page,
        translations__language_code=language,
        slug=slug,
        status=Page.Status.PUBLISHED,
    )
    return render(
        request,
        "pages/page.html",
        {"object": home}
    )
