from django.urls import resolve



def site_options(request):
    options = SiteOptions.get_options()
    return {"site_options": options}


def language_flag_map(request):
    from django.conf import settings
    return {"LANGUAGE_FLAG_MAP": settings.LANGUAGE_FLAG_MAP}
