from django.contrib import admin
from .models import Exhibition, Event


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "start_date",
        "end_date",
        "is_permanent",
        "is_active",
    )

    list_filter = (
        "category",
        "is_permanent",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "event_type",
        "date",
        "time",
        "location",
        "is_active",
    )

    list_filter = (
        "event_type",
        "date",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
        "location",
    )

