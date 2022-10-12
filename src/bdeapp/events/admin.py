from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _, ngettext

from bdeapp.events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": ("uuid", "name", "date", "time", "published"),
            },
        ),
        (_("Description"), {"fields": ("description", "long_description")}),
        (
            _("Links"),
            {"fields": ("facebook_link", "instagram_link", "maps_link", "misc_link")},
        ),
    )

    date_hierarchy = "date"
    list_display = ("name", "merge_datetime", "description", "published")
    list_filter = ("published", "date")
    readonly_fields = ("uuid",)
    search_fields = ("name", "description")
    actions = ("make_published",)

    @admin.display(description=_("Event date"), ordering="-date")
    def merge_datetime(self, obj) -> str:
        return f"{obj.date}{f' ({obj.time})' if obj.time else ''}"

    @admin.action(description=_("Mark as published"))
    def make_published(self, request, queryset):
        updated = queryset.update(published=True)
        self.message_user(
            request,
            ngettext(
                "%d event was successfully marked as published.",
                "%d events were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
