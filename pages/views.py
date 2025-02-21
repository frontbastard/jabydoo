from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils.translation import get_language
from django.views.generic import DetailView

from games.models import Game
from .models import Page


class PageDetailView(DetailView):
    model = Page
    template_name = "page_detail.html"
    context_object_name = "page"

    def get_object(self):
        lang = get_language()
        slug = self.kwargs.get("slug")

        if not slug:
            home_page = Page.objects.get_home_page()
            if not home_page:
                return render(self.request, "404.html", status=404)
            return home_page.translated(lang)

        return get_object_or_404(Page.objects.get_published().translated(lang), slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["games"] = Game.objects.all()

        return context
