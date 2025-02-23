from django.conf import settings
from django.contrib.sites.models import Site

from .models import SiteOptions

import base64


def site_options(request):
    options_obj = SiteOptions.get_options()
    options = vars(options_obj) if options_obj else {}
    sponsor_url = options.get("sponsor_url", "")
    site = Site.objects.get_current()

    options["site_domain"] = site.domain
    options["site_name"] = settings.SITE_NAME

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
    return {"LANGUAGE_FLAG_MAP": getattr(settings, "LANGUAGE_FLAG_MAP", {})}
