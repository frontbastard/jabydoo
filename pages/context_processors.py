from .models import Page


def all_pages(request):
    return {"all_pages": Page.objects.filter(
        is_home=False,
        status=Page.Status.PUBLISHED
    )}
