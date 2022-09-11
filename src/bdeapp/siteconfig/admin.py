from django.contrib import admin

from solo.admin import SingletonModelAdmin

from bdeapp.siteconfig.models import SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    pass
