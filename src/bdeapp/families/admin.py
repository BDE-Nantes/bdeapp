from django.contrib import admin

from bdeapp.families.models import Family


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    fields = ("uuid", "name", "image")

    def has_add_permission(self, request) -> bool:
        return Family.can_add_family()
