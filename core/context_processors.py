from django.urls import resolve


def current_url_name(request):
    resolved_url = resolve(request.path_info)
    return {"current_url_name": resolved_url.url_name}


def language_flag_map(request):
    from django.conf import settings
    return {"LANGUAGE_FLAG_MAP": settings.LANGUAGE_FLAG_MAP}
