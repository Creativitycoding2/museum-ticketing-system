from ..models import Exhibition, Event, Booking, Visit
from ..services import book_event, book_general_visit, cancel_booking
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime


def get_exhibitions():
    exhibitions = Exhibition.objects.filter(
        is_active=True
    ).order_by("-created_at")

    return [
        {
            "id": exhibition.id,
            "title": exhibition.title,
            "category": exhibition.category,
            "description": exhibition.description,
            "start_date": exhibition.start_date.isoformat()
            if exhibition.start_date else None,
            "end_date": exhibition.end_date.isoformat()
            if exhibition.end_date else None,
            "is_permanent": exhibition.is_permanent,
        }
        for exhibition in exhibitions
    ]


def get_exhibition_details(exhibition_id):
    exhibition = Exhibition.objects.filter(
        id=exhibition_id,
        is_active=True
    ).first()

    if not exhibition:
        return {
            "error": "Exhibition not found."
        }

    return {
        "id": exhibition.id,
        "title": exhibition.title,
        "category": exhibition.category,
        "description": exhibition.description,
        "start_date": exhibition.start_date.isoformat()
        if exhibition.start_date else None,
        "end_date": exhibition.end_date.isoformat()
        if exhibition.end_date else None,
        "is_permanent": exhibition.is_permanent,
        "image": exhibition.image,
    }


def get_upcoming_events():
    today = timezone.localdate()

    events = Event.objects.filter(
        is_active=True,
        date__gte=today
    ).order_by("date", "time")

    return [
        {
            "id": event.id,
            "title": event.title,
            "event_type": event.event_type,
            "description": event.description,
            "date": event.date.isoformat(),
            "time": event.time.isoformat(),
            "location": event.location,
            "capacity": event.capacity,
        }
        for event in events
    ]


def get_event_details(event_id):
    event = Event.objects.filter(
        id=event_id,
        is_active=True
    ).first()

    if not event:
        return {
            "error": "Event not found."
        }

    return {
        "id": event.id,
        "title": event.title,
        "event_type": event.event_type,
        "description": event.description,
        "date": event.date.isoformat(),
        "time": event.time.isoformat(),
        "location": event.location,
        "capacity": event.capacity,
    }


def check_event_availability(event_id):
    event = Event.objects.filter(
        id=event_id,
        is_active=True
    ).first()

    if not event:
        return {
            "error": "Event not found."
        }

    if event.capacity is None:
        return {
            "event_id": event.id,
            "title": event.title,
            "capacity": None,
            "booked_tickets": sum(
                booking.number_of_tickets
                for booking in event.bookings.filter(status="active")
            ),
            "remaining_tickets": None,
            "availability": "Available",
        }

    booked_tickets = sum(
        booking.number_of_tickets
        for booking in event.bookings.filter(status="active")
    )

    remaining_tickets = max(
        event.capacity - booked_tickets,
        0
    )

    return {
        "event_id": event.id,
        "title": event.title,
        "capacity": event.capacity,
        "booked_tickets": booked_tickets,
        "remaining_tickets": remaining_tickets,
        "availability": (
            "Available"
            if remaining_tickets > 0
            else "Sold out"
        ),
    }


def get_my_bookings(user):
    event_bookings = Booking.objects.filter(
        user=user
    ).select_related("event").order_by("-booked_at")

    visits = Visit.objects.filter(
        user=user
    ).order_by("-booked_at")

    return {
        "event_bookings": [
            {
                "booking_id": booking.id,
                "ticket_id": str(booking.ticket_id),
                "event_id": booking.event.id,
                "event_title": booking.event.title,
                "number_of_tickets": booking.number_of_tickets,
                "status": booking.status,
                "event_date": booking.event.date.isoformat(),
                "event_time": booking.event.time.isoformat(),
                "booked_at": booking.booked_at.isoformat(),
            }
            for booking in event_bookings
        ],
        "general_visits": [
            {
                "visit_id": visit.id,
                "ticket_id": str(visit.ticket_id),
                "date": visit.date.isoformat(),
                "time": visit.time.isoformat(),
                "number_of_visitors": visit.number_of_visitors,
                "status": visit.status,
                "booked_at": visit.booked_at.isoformat(),
            }
            for visit in visits
        ],
    }


def ai_book_event(user, event_id, number_of_tickets):
    try:
        booking = book_event(
            user=user,
            event_id=event_id,
            number_of_tickets=number_of_tickets
        )

        return {
            "success": True,
            "booking_id": booking.id,
            "ticket_id": str(booking.ticket_id),
            "event_id": booking.event.id,
            "event_title": booking.event.title,
            "number_of_tickets": booking.number_of_tickets,
            "status": booking.status,
        }

    except ValidationError as e:
        return {
            "success": False,
            "error": str(e),
        }


def ai_book_general_visit(
    user,
    date,
    time,
    number_of_visitors
):
    try:
        date = datetime.strptime(
            date,
            "%Y-%m-%d"
        ).date()

        time = datetime.strptime(
            time,
            "%H:%M"
        ).time()

        visit = book_general_visit(
            user=user,
            date=date,
            time=time,
            number_of_visitors=number_of_visitors
        )

        return {
            "success": True,
            "visit_id": visit.id,
            "ticket_id": str(visit.ticket_id),
            "date": visit.date.isoformat(),
            "time": visit.time.isoformat(),
            "number_of_visitors": visit.number_of_visitors,
            "status": visit.status,
        }

    except (ValidationError, ValueError) as e:
        return {
            "success": False,
            "error": str(e),
        }


def ai_cancel_booking(user, booking_id):
    try:
        cancel_booking(
            user=user,
            booking_id=booking_id
        )

        return {
            "success": True,
            "booking_id": booking_id,
            "status": "cancelled",
        }

    except ValidationError as e:
        return {
            "success": False,
            "error": str(e),
        }


GET_EXHIBITIONS_TOOL = {
    "name": "get_exhibitions",
    "description": "Get all currently active museum exhibitions.",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}
GET_EXHIBITION_DETAILS_TOOL = {
    "name": "get_exhibition_details",
    "description": "Get detailed information about a specific active museum exhibition.",
    "parameters": {
        "type": "object",
        "properties": {
            "exhibition_id": {
                "type": "integer",
                "description": "The ID of the exhibition."
            }
        },
        "required": ["exhibition_id"],
    },
}
GET_UPCOMING_EVENTS_TOOL = {
    "name": "get_upcoming_events",
    "description": "Get all upcoming active museum events.",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}
GET_EVENT_DETAILS_TOOL = {
    "name": "get_event_details",
    "description": "Get detailed information about a specific active museum event.",
    "parameters": {
        "type": "object",
        "properties": {
            "event_id": {
                "type": "integer",
                "description": "The ID of the event."
            }
        },
        "required": ["event_id"],
    },
}
CHECK_EVENT_AVAILABILITY_TOOL = {
    "name": "check_event_availability",
    "description": "Check the current ticket availability for a specific active museum event.",
    "parameters": {
        "type": "object",
        "properties": {
            "event_id": {
                "type": "integer",
                "description": "The ID of the event."
            }
        },
        "required": ["event_id"],
    },
}
GET_MY_BOOKINGS_TOOL = {
    "name": "get_my_bookings",
    "description": "Get the currently logged-in user's museum event bookings and general visit bookings.",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}
BOOK_EVENT_TOOL = {
    "name": "book_event",
    "description": "Book tickets for a specific museum event for the currently logged-in user.",
    "parameters": {
        "type": "object",
        "properties": {
            "event_id": {
                "type": "integer",
                "description": "The ID of the event to book."
            },
            "number_of_tickets": {
                "type": "integer",
                "description": "The number of tickets to book."
            },
        },
        "required": ["event_id", "number_of_tickets"],
    },
}
BOOK_GENERAL_VISIT_TOOL = {
    "name": "book_general_visit",
    "description": "Book a general museum visit for the currently logged-in user.",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "The visit date in YYYY-MM-DD format."
            },
            "time": {
                "type": "string",
                "description": "The visit time in HH:MM format."
            },
            "number_of_visitors": {
                "type": "integer",
                "description": "The number of visitors."
            },
        },
        "required": ["date", "time", "number_of_visitors"],
    },
}
CANCEL_BOOKING_TOOL = {
    "name": "cancel_booking",
    "description": "Cancel an active event booking belonging to the currently logged-in user.",
    "parameters": {
        "type": "object",
        "properties": {
            "booking_id": {
                "type": "integer",
                "description": "The ID of the booking to cancel."
            },
        },
        "required": ["booking_id"],
    },
}

TOOL_REGISTRY = {
    "get_exhibitions": get_exhibitions,
    "get_exhibition_details": get_exhibition_details,
    "get_upcoming_events": get_upcoming_events,
    "get_event_details": get_event_details,
    "check_event_availability": check_event_availability,
    "get_my_bookings": get_my_bookings,
    "book_event": ai_book_event,
    "book_general_visit": ai_book_general_visit,
    "cancel_booking": ai_cancel_booking,
}
TOOL_DECLARATIONS = [
    GET_EXHIBITIONS_TOOL,
    GET_EXHIBITION_DETAILS_TOOL,
    GET_UPCOMING_EVENTS_TOOL,
    GET_EVENT_DETAILS_TOOL,
    CHECK_EVENT_AVAILABILITY_TOOL,
    GET_MY_BOOKINGS_TOOL,
    BOOK_EVENT_TOOL,
    BOOK_GENERAL_VISIT_TOOL,
    CANCEL_BOOKING_TOOL,
]
