from django.contrib import admin

from solo.admin import SingletonModelAdmin

from bdeapp.siteconfig.models import RedirectLink, SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    pass


@admin.register(RedirectLink)
class RedirectLinkAdmin(admin.ModelAdmin):
    list_display = ("url_slug", "url")
    search_fields = ("url_slug", "url")
