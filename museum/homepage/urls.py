from django.urls import path
from . import views

urlpatterns = [

    # Public
    path("", views.home, name="home"),
    path("exhibitions/", views.exhibitions, name="exhibitions"),
    path("events/", views.events, name="events"),

    # Admin dashboard
    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "admin-dashboard/exhibitions/add/",
        views.add_exhibition,
        name="add_exhibition"
    ),

    path(
        "admin-dashboard/events/add/",
        views.add_event,
        name="add_event"
    ),
    path(
        "admin-dashboard/exhibitions/",
        views.manage_exhibitions,
        name="manage_exhibitions",
    ),

    path(
        "admin-dashboard/exhibitions/<int:exhibition_id>/deactivate/",
        views.deactivate_exhibition,
        name="deactivate_exhibition",
    ),

    path(
        "admin-dashboard/events/",
        views.manage_events,
        name="manage_events",
    ),

    path(
        "admin-dashboard/events/<int:event_id>/deactivate/",
        views.deactivate_event,
        name="deactivate_event",
    ),
    path(
        "admin-dashboard/exhibitions/<int:exhibition_id>/edit/",
        views.edit_exhibition,
        name="edit_exhibition",
    ),

    path(
        "admin-dashboard/events/<int:event_id>/edit/",
        views.edit_event,
        name="edit_event",
    )
]
