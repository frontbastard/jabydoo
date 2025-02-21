import base64

from .models import SiteOptions

import base64


def site_options(request):
    options_obj = SiteOptions.get_options()
    options = vars(options_obj) if options_obj else {}
    sponsor_url = options.get("sponsor_url", "")

    # Add a field to check if the URL needs to be hidden
    options["hide_sponsor_url"] = options_obj.hide_sponsor_url if options_obj else True

    # Mask the URL, if necessary
    options["sponsor_encoded_url"] = (
        base64.b64encode(sponsor_url.encode("utf-8")).decode("utf-8")
        if sponsor_url and options["hide_sponsor_url"]
        else sponsor_url
    )

    options["sponsor_logo"] = (
        options_obj.sponsor_logo.url if options_obj and options_obj.sponsor_logo else ""
    )

    return {"site_options": options}


def language_flag_map(request):
    from django.conf import settings
    return {"LANGUAGE_FLAG_MAP": settings.LANGUAGE_FLAG_MAP}
