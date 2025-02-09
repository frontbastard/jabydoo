from django.conf import settings

from core.models import SiteOptions


def site_options(request):
    options = SiteOptions.get_options()
    return {"site_options": options}


def language_flag_map(request):
    from django.conf import settings
    return {"LANGUAGE_FLAG_MAP": settings.LANGUAGE_FLAG_MAP}


def environment_processor(request):
    return {"ENVIRONMENT": settings.ENVIRONMENT}
