from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from .models import Exhibition, Event
from .forms import ExhibitionForm, EventForm


def is_staff(user):
    return user.is_authenticated and user.is_staff


@login_required()
@user_passes_test(is_staff)
def admin_dashboard(request):

    total_exhibitions = Exhibition.objects.count()

    active_exhibitions = Exhibition.objects.filter(
        is_active=True
    ).count()

    total_events = Event.objects.count()

    upcoming_events = Event.objects.filter(
        is_active=True
    ).count()

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
