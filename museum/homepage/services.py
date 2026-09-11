from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Event, Booking, Visit


def book_event(user, event_id, number_of_tickets):
    event = Event.objects.filter(
        id=event_id,
        is_active=True
    ).first()

    if not event:
        raise ValidationError("Event not found.")

    if number_of_tickets < 1:
        raise ValidationError(
            "Number of tickets must be at least 1."
        )

    if event.date < timezone.localdate():
        raise ValidationError(
            "This event has already taken place."
        )

    if event.capacity is not None:
        booked_tickets = sum(
            booking.number_of_tickets
            for booking in event.bookings.filter(
                status="active"
            )
        )

        remaining_tickets = event.capacity - booked_tickets

        if number_of_tickets > remaining_tickets:
            raise ValidationError(
                f"Only {remaining_tickets} tickets are available."
            )

    booking = Booking.objects.create(
        event=event,
        user=user,
        number_of_tickets=number_of_tickets
    )

    return booking


def cancel_booking(user, booking_id):
    booking = Booking.objects.filter(
        id=booking_id,
        user=user,
        status="active"
    ).first()

    if not booking:
        raise ValidationError(
            "Active booking not found."
        )

    booking.status = "cancelled"
    booking.save(update_fields=["status"])

    return True


def book_general_visit(
    user,
    date,
    time,
    number_of_visitors
):
    if number_of_visitors < 1:
        raise ValidationError(
            "Number of visitors must be at least 1."
        )

    today = timezone.localdate()

    if date < today:
        raise ValidationError(
            "You cannot book a visit for a past date."
        )

    visit = Visit.objects.create(
        user=user,
        date=date,
        time=time,
        number_of_visitors=number_of_visitors
    )

    return visit


def cancel_visit(user, visit_id):
    visit = Visit.objects.filter(
        id=visit_id,
        user=user,
        status="active"
    ).first()

    if not visit:
        raise ValidationError(
            "Active visit booking not found."
        )

    visit.status = "cancelled"
    visit.save(update_fields=["status"])

    return True


def verify_ticket(ticket_id):
    booking = Booking.objects.filter(
        ticket_id=ticket_id
    ).select_related("user", "event").first()

    if booking:
        return {
            "type": "event",
            "valid": booking.status == "active",
            "status": booking.status,
            "ticket": booking,
        }

    visit = Visit.objects.filter(
        ticket_id=ticket_id
    ).select_related("user").first()

    if visit:
        return {
            "type": "visit",
            "valid": visit.status == "active",
            "status": visit.status,
            "ticket": visit,
        }

    return {
        "type": None,
        "valid": False,
        "status": "not_found",
        "ticket": None,
    }


def mark_ticket_used(ticket_id):
    result = verify_ticket(ticket_id)

    if result["status"] == "not_found":
        raise ValidationError("Ticket not found.")

    if result["status"] == "cancelled":
        raise ValidationError("This ticket has been cancelled.")

    if result["status"] == "used":
        raise ValidationError("This ticket has already been used.")

    ticket = result["ticket"]

    ticket.status = "used"
    ticket.save(update_fields=["status"])

    return ticket
