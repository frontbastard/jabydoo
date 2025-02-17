from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from games.models import Game
from .models import Page


def home_page(request):
    home = Page.objects.filter(
        is_home=True, status=Page.Status.PUBLISHED
    ).order_by("-is_home").first()
    games = Game.objects.all()

    if not home:
        home = Page.objects.filter(status=Page.Status.PUBLISHED).first()

    if not home:
        return render(request, "/pages/404.html", status=404)

    return render(
        request,
        "pages/home.html",
        {"object": home, "games": games}
    )


def other_page(request, slug):
    language = request.LANGUAGE_CODE
    page = get_object_or_404(
        Page,
        translations__language_code=language,
        slug=slug,
        status=Page.Status.PUBLISHED,
    )
    games = Game.objects.all()
    return render(
        request,
        "pages/page.html",
        {"object": page, "games": games}
    )
