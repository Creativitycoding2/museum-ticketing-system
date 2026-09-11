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
    ),
    path(
        "exhibitions/<int:exhibition_id>/",
        views.exhibition_detail,
        name="exhibition_detail"
    ),
    path(
        "events/<int:event_id>/",
        views.event_detail,
        name="event_detail"
    ),
    path(
        "events/<int:event_id>/book/",
        views.book_event_view,
        name="book_event"
    ),
    path(
        "my-bookings/",
        views.my_bookings,
        name="my_bookings"
    ),
    path(
        "my-bookings/event/<int:booking_id>/cancel/",
        views.cancel_booking_view,
        name="cancel_booking"
    ),

    path(
        "my-bookings/visit/<int:visit_id>/cancel/",
        views.cancel_visit_view,
        name="cancel_visit"
    ),
    path(
        "ticket/<str:ticket_type>/<uuid:ticket_id>/qr/",
        views.ticket_qr,
        name="ticket_qr"
    ),
    path(
        "staff/ticket/<uuid:ticket_id>/verify/",
        views.verify_ticket_view,
        name="verify_ticket"
    ),
    path(
        "staff/ticket-scanner/",
        views.ticket_scanner,
        name="ticket_scanner"
    ),
    path(
        "admin-dashboard/bookings/",
        views.manage_bookings,
        name="manage_bookings"
    ),
    path(
        "staff/ticket/<uuid:ticket_id>/check-in/",
        views.check_in_ticket_view,
        name="check_in_ticket"
    ),
    path("chatbot/", views.chatbot, name="chatbot"),
    path("chatbot/confirm/", views.confirm_ai_action, name="confirm_ai_action"),
    path("chatbot/cancel/", views.cancel_ai_action, name="cancel_ai_action"),
]
