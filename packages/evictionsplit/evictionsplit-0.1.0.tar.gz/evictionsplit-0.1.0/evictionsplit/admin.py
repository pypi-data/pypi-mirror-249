from django.contrib import admin
from django.utils.html import format_html

from .models import Clocking, Eviction


@admin.register(Eviction)
class EvictionAdmin(admin.ModelAdmin):
    fields = ["name", "creator", "active", "participants", "applicants"]
    readonly_fields = ["creator", "participants", "applicants"]

    def save_model(self, request, obj, form, change):
        if getattr(obj, "creator", None) is None:
            obj.creator = request.user
            super().save_model(request, obj, form, change)
            obj.participants.add(request.user)
        super().save_model(request, obj, form, change)


@admin.action(description="Stop selected clocking")
def stop_clockings(modeladmin, request, queryset):
    for clocking in queryset:
        clocking.stop()


class CurrentlyOnDutyFilter(admin.SimpleListFilter):
    title = "currently on duty"
    parameter_name = "on_duty"

    def lookups(self, request, model_admin):
        return [
            ("True", "Active right now"),
            ("False", "Inactive right now"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(end__isnull=True)
        if self.value() == "False":
            return queryset.filter(end__isnull=False)


@admin.register(Clocking)
class ClockingAdmin(admin.ModelAdmin):
    @admin.display(description="Eviction name")
    def eviction_name(self, obj):
        return obj.eviction.name

    @admin.display(description="")
    def _character_pic(self, obj):
        return format_html(
            '<img src="{}" class="img-circle">',
            obj.eviction.creator.profile.main_character.portrait_url(size=32),
        )

    @admin.display(description="Character name")
    def _character_name(self, obj):
        return obj.eviction.creator.profile.main_character.character_name

    fields = ["user", "eviction", "type", ("beginning", "end")]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["user", "eviction"]
        else:
            return []

    list_display = [
        "_character_pic",
        "_character_name",
        "type",
        "beginning",
        "end",
        "eviction",
    ]
    list_filter = [
        "eviction",
        "user",
        "type",
        CurrentlyOnDutyFilter,
    ]  # TODO turn the "by user" to a "by character"

    actions = [stop_clockings]
