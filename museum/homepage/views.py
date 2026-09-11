from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q, Sum
from django.utils import timezone
from .models import Exhibition, Event, Booking, Visit
from .forms import ExhibitionForm, EventForm
from .services import book_event, cancel_booking, cancel_visit, verify_ticket, mark_ticket_used
from django.core.exceptions import ValidationError
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from .ticket_utils import generate_ticket_qr
from .ai.client import ask_gemini
from .ai.tools import ai_cancel_booking, ai_book_event, ai_book_general_visit
from datetime import timedelta, datetime


def is_staff(user):
    return user.is_authenticated and user.is_staff


@login_required()
@user_passes_test(is_staff)
def admin_dashboard(request):

    today = timezone.localdate()

    total_exhibitions = Exhibition.objects.count()

    active_exhibitions = Exhibition.objects.filter(
        is_active=True
    ).count()

    total_events = Event.objects.count()

    upcoming_events = Event.objects.filter(
        is_active=True,
        date__gte=today
    ).count()

    total_event_bookings = Booking.objects.count()

    active_event_bookings = Booking.objects.filter(
        status="active"
    ).count()

    total_visits = Visit.objects.count()

    active_visits = Visit.objects.filter(
        status="active"
    ).count()

    total_active_tickets = (
        active_event_bookings +
        active_visits
    )

    recent_exhibitions = Exhibition.objects.order_by(
        "-created_at"
    )[:5]

    recent_events = Event.objects.order_by(
        "-created_at"
    )[:5]

    context = {
        "total_exhibitions": total_exhibitions,
        "active_exhibitions": active_exhibitions,
        "total_events": total_events,
        "upcoming_events": upcoming_events,

        "total_event_bookings": total_event_bookings,
        "active_event_bookings": active_event_bookings,
        "total_visits": total_visits,
        "active_visits": active_visits,
        "total_active_tickets": total_active_tickets,

        "recent_exhibitions": recent_exhibitions,
        "recent_events": recent_events,
    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )


@login_required
@user_passes_test(is_staff)
def add_exhibition(request):

    if request.method == "POST":
        form = ExhibitionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")

    else:
        form = ExhibitionForm()

    return render(
        request,
        "exhibition_form.html",
        {"form": form}
    )


@login_required
@user_passes_test(is_staff)
def manage_exhibitions(request):
    exhibitions = Exhibition.objects.order_by("-created_at")

    return render(
        request,
        "exhibitions_admin.html",
        {"exhibitions": exhibitions}
    )


@login_required
@user_passes_test(is_staff)
def deactivate_exhibition(request, exhibition_id):

    if request.method == "POST":
        exhibition = Exhibition.objects.get(id=exhibition_id)
        exhibition.is_active = False
        exhibition.save()

    return redirect("manage_exhibitions")


@login_required
@user_passes_test(is_staff)
def add_event(request):

    if request.method == "POST":
        form = EventForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")

    else:
        form = EventForm()

    return render(
        request,
        "event_form.html",
        {"form": form}
    )


@login_required
@user_passes_test(is_staff)
def manage_events(request):
    events = Event.objects.order_by("date", "time")

    return render(
        request,
        "events_admin.html",
        {"events": events}
    )


@login_required
@user_passes_test(is_staff)
def deactivate_event(request, event_id):

    if request.method == "POST":
        event = Event.objects.get(id=event_id)
        event.is_active = False
        event.save()

    return redirect("manage_events")


@login_required
@user_passes_test(is_staff)
def edit_exhibition(request, exhibition_id):
    exhibition = get_object_or_404(Exhibition, id=exhibition_id)

    if request.method == "POST":
        form = ExhibitionForm(request.POST, instance=exhibition)

        if form.is_valid():
            form.save()
            return redirect("manage_exhibitions")
    else:
        form = ExhibitionForm(instance=exhibition)

    return render(
        request,
        "exhibition_form.html",
        {
            "form": form,
            "editing": True,
        }
    )


@login_required
@user_passes_test(is_staff)
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)

        if form.is_valid():
            form.save()
            return redirect("manage_events")
    else:
        form = EventForm(instance=event)

    return render(
        request,
        "event_form.html",
        {
            "form": form,
            "editing": True,
        }
    )


def home(request):
    exhibitions = Exhibition.objects.filter(
        is_active=True
    ).order_by("-created_at")[:3]

    events = Event.objects.filter(
        is_active=True
    ).order_by("date", "time")[:3]

    return render(
        request,
        "home.html",
        {
            "exhibitions": exhibitions,
            "events": events,
        }
    )


@login_required
def exhibitions(request):
    exhibitions = Exhibition.objects.filter(
        is_active=True
    ).order_by("-created_at")

    return render(
        request,
        "exibitions.html",
        {"exhibitions": exhibitions}
    )


@login_required
def events(request):
    events = Event.objects.filter(
        is_active=True
    ).order_by("date", "time")

    return render(
        request,
        "events.html",
        {"events": events}
    )


@login_required
def exhibition_detail(request, exhibition_id):
    exhibition = get_object_or_404(
        Exhibition,
        id=exhibition_id,
        is_active=True
    )

    return render(
        request,
        "exhibition_detail.html",
        {"exhibition": exhibition}
    )


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(
        Event,
        id=event_id,
        is_active=True
    )

    return render(
        request,
        "event_detail.html",
        {"event": event}
    )


@login_required
def book_event_view(request, event_id):

    if request.method != "POST":
        return redirect(
            "event_detail",
            event_id=event_id
        )

    try:
        number_of_tickets = int(
            request.POST.get(
                "number_of_tickets",
                1
            )
        )

        booking = book_event(
            user=request.user,
            event_id=event_id,
            number_of_tickets=number_of_tickets
        )

    except ValueError:
        return redirect(
            "event_detail",
            event_id=event_id
        )

    except ValidationError:
        return redirect(
            "event_detail",
            event_id=event_id
        )

    return redirect(
        "event_detail",
        event_id=booking.event.id
    )


@login_required
def my_bookings(request):
    event_bookings = Booking.objects.filter(
        user=request.user
    ).select_related("event")

    visits = Visit.objects.filter(
        user=request.user
    )

    return render(
        request,
        "my_bookings.html",
        {
            "event_bookings": event_bookings,
            "visits": visits,
        }
    )


@login_required
def cancel_booking_view(request, booking_id):

    if request.method != "POST":
        return redirect("my_bookings")

    try:
        cancel_booking(
            user=request.user,
            booking_id=booking_id
        )
    except ValidationError:
        pass

    return redirect("my_bookings")


@login_required
def cancel_visit_view(request, visit_id):

    if request.method != "POST":
        return redirect("my_bookings")

    try:
        cancel_visit(
            user=request.user,
            visit_id=visit_id
        )
    except ValidationError:
        pass

    return redirect("my_bookings")


@login_required
def ticket_qr(request, ticket_type, ticket_id):

    if ticket_type == "event":
        ticket = Booking.objects.filter(
            user=request.user,
            ticket_id=ticket_id
        ).first()

    elif ticket_type == "visit":
        ticket = Visit.objects.filter(
            user=request.user,
            ticket_id=ticket_id
        ).first()

    else:
        return HttpResponse(
            "Invalid ticket type.",
            status=400
        )

    if not ticket:
        return HttpResponse(
            "Ticket not found.",
            status=404
        )

    qr_image = generate_ticket_qr(ticket.ticket_id)

    buffer = BytesIO()
    qr_image.save(buffer, format="PNG")

    return HttpResponse(
        buffer.getvalue(),
        content_type="image/png"
    )


@login_required
@user_passes_test(is_staff)
def verify_ticket_view(request, ticket_id):
    result = verify_ticket(ticket_id)

    return JsonResponse({
        "valid": result["valid"],
        "status": result["status"],
        "type": result["type"],
    })


@login_required
@user_passes_test(is_staff)
def ticket_scanner(request):
    return render(
        request,
        "ticket_scanner.html"
    )


@login_required
@user_passes_test(is_staff)
def manage_bookings(request):
    status = request.GET.get("status", "all")

    event_bookings = Booking.objects.select_related(
        "user",
        "event"
    ).order_by("-booked_at")

    visits = Visit.objects.select_related(
        "user"
    ).order_by("-booked_at")

    if status in ["active", "cancelled", "used"]:
        event_bookings = event_bookings.filter(status=status)
        visits = visits.filter(status=status)

    return render(
        request,
        "manage_bookings.html",
        {
            "event_bookings": event_bookings,
            "visits": visits,
            "current_status": status,
        }
    )


@login_required
@user_passes_test(is_staff)
def check_in_ticket_view(request, ticket_id):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required."},
            status=405
        )

    try:
        ticket = mark_ticket_used(ticket_id)

    except ValidationError as e:
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=400
        )

    return JsonResponse({
        "success": True,
        "status": ticket.status,
    })


@login_required
def chatbot(request):

    if request.method == "GET":
        return render(request, "chatbot.html")

    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed."},
            status=405
        )

    message = request.POST.get("message", "").strip()

    if not message:
        return JsonResponse(
            {"error": "Message is required."},
            status=400
        )
    conversation_history = request.session.get(
        "conversation_history",
        []
    )

    try:

        response = ask_gemini(
            message,
            user=request.user,
            conversation_history=conversation_history
        )

    except Exception as e:

        return JsonResponse(
            {"error": str(e)},
            status=500
        )

    if isinstance(response, dict) and response.get(
        "confirmation_required"
    ):

        action = response["action"]
        arguments = response["arguments"]

        confirmation_message = build_ai_confirmation(
            request,
            action,
            arguments
        )
        conversation_history.append({
            "role": "user",
            "content": message,
        })

        conversation_history.append({
            "role": "assistant",
            "content": confirmation_message,
        })

        conversation_history = conversation_history[-10:]

        request.session["conversation_history"] = conversation_history

        if not confirmation_message:

            return JsonResponse(
                {"error": "Unable to prepare this action."},
                status=400
            )

        request.session["pending_ai_action"] = {
            "action": action,
            "arguments": arguments,
            "created_at": timezone.now().isoformat(),
            "user_id": request.user.id,
        }

        return JsonResponse({
            "confirmation_required": True,
            "message": confirmation_message,
        })

    conversation_history.append({
        "role": "user",
        "content": message,
    })

    conversation_history.append({
        "role": "assistant",
        "content": response,
    })

    conversation_history = conversation_history[-10:]

    request.session["conversation_history"] = conversation_history

    return JsonResponse({
        "response": response
    })


@login_required
def confirm_ai_action(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required."},
            status=405
        )

    pending_action = request.session.get("pending_ai_action")

    if not pending_action:
        return JsonResponse(
            {"error": "No pending action found."},
            status=400
        )

    created_at = datetime.fromisoformat(
        pending_action["created_at"]
    )

    if timezone.now() - created_at > timedelta(minutes=10):
        request.session.pop(
            "pending_ai_action",
            None
        )

        return JsonResponse(
            {
                "error":
                    "This confirmation has expired. "
                    "Please request the action again."
            },
            status=400
        )
    if pending_action.get("user_id") != request.user.id:
        request.session.pop(
            "pending_ai_action",
            None
        )

        return JsonResponse(
            {"error": "Invalid pending action."},
            status=400
        )
    action = pending_action["action"]
    arguments = pending_action["arguments"]

    allowed_actions = {
        "book_event": ai_book_event,
        "book_general_visit": ai_book_general_visit,
        "cancel_booking": ai_cancel_booking,
    }

    function = allowed_actions.get(action)

    if not function:
        request.session.pop("pending_ai_action", None)

        return JsonResponse(
            {"error": "Invalid pending action."},
            status=400
        )
    if not isinstance(arguments, dict):
        request.session.pop("pending_ai_action", None)

        return JsonResponse(
            {"error": "Invalid action arguments."},
            status=400
        )
    if action == "book_event":

        if (
                not isinstance(arguments.get("event_id"), int)
                or not isinstance(arguments.get("number_of_tickets"), int)
                or arguments["number_of_tickets"] < 1
        ):
            request.session.pop("pending_ai_action", None)

            return JsonResponse(
                {"error": "Invalid booking arguments."},
                status=400
            )

    elif action == "book_general_visit":

        if (
                not isinstance(arguments.get("date"), str)
                or not isinstance(arguments.get("time"), str)
                or not isinstance(arguments.get("number_of_visitors"), int)
                or arguments["number_of_visitors"] < 1
        ):
            request.session.pop("pending_ai_action", None)

            return JsonResponse(
                {"error": "Invalid visit arguments."},
                status=400
            )

    elif action == "cancel_booking":

        if not isinstance(arguments.get("booking_id"), int):
            request.session.pop("pending_ai_action", None)

            return JsonResponse(
                {"error": "Invalid cancellation arguments."},
                status=400
            )
    arguments["user"] = request.user

    try:
        result = function(**arguments)

    except Exception as e:
        request.session.pop("pending_ai_action", None)

        return JsonResponse(
            {"error": str(e)},
            status=400
        )

    request.session.pop("pending_ai_action", None)

    return JsonResponse({
        "success": True,
        "result": result,
    })


def build_ai_confirmation(request, action, arguments):
    if action == "book_event":
        event = Event.objects.filter(
            id=arguments["event_id"],
            is_active=True
        ).first()

        if not event:
            return None

        return (
            f'Book {arguments["number_of_tickets"]} ticket(s) '
            f'for "{event.title}" on '
            f'{event.date.strftime("%B %d, %Y")} at '
            f'{event.time.strftime("%I:%M %p")}?'
        )

    if action == "book_general_visit":
        return (
            f'Book a general museum visit for '
            f'{arguments["number_of_visitors"]} visitor(s) on '
            f'{arguments["date"]} at {arguments["time"]}?'
        )

    if action == "cancel_booking":
        booking = Booking.objects.filter(
            id=arguments["booking_id"],
            user=request.user,
            status="active"
        ).select_related("event").first()

        if not booking:
            return None

        return (
            f'Cancel your booking for "{booking.event.title}" '
            f'with {booking.number_of_tickets} ticket(s)?'
        )

    return None


@login_required
def cancel_ai_action(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required."},
            status=405
        )

    pending_action = request.session.get("pending_ai_action")

    if not pending_action:
        return JsonResponse(
            {"error": "No pending action found."},
            status=400
        )

    request.session.pop("pending_ai_action", None)

    return JsonResponse({
        "success": True,
        "message": "Action cancelled."
    })
