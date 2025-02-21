from django.contrib.sites.models import Site
from django.conf import settings


class UpdateSiteDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.update_site_domain()

    def __call__(self, request):
        return self.get_response(request)

    def update_site_domain(self):
        if not hasattr(settings, "SITE_DOMAIN"):
            return

        try:
            site = Site.objects.get_current()
            new_domain = settings.SITE_DOMAIN
            new_name = settings.SITE_NAME

            if site.domain != new_domain:
                site.domain = new_domain
                site.name = new_name
                site.save()
                print(f"[INFO] Updated Site.domain to {new_domain}")
            else:
                print(f"[INFO] Site.domain is already equal to {new_domain}")

        except Site.DoesNotExist:
            print("[WARNING] Site not found")
