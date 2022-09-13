from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from bdeapp.siteconfig.models import RedirectLink


class LinkRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        redirect_link = get_object_or_404(RedirectLink, url_slug=kwargs["slug"])
        return redirect_link.url
