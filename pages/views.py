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
            return self.get_home_page(lang)

        return get_object_or_404(Page.objects.get_published().translated(lang), slug=slug)

    def get_home_page(self, lang):
        home_page = Page.objects.get_home_page()
        if not home_page:
            raise Http404("Головна сторінка не знайдена")

        return Page.objects.get_published().filter(pk=home_page.pk).translated(lang).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["games"] = Game.objects.all()
        return context
