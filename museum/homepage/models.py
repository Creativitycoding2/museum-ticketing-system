from django.db import models
from django.urls import reverse
from django.conf import settings
import uuid


class Exhibition(models.Model):
    CATEGORY_CHOICES = [
        ("History", "History"),
        ("Art", "Art"),
        ("Science", "Science"),
        ("Culture", "Culture"),
        ("Other", "Other"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="Other"
    )
    description = models.TextField()
    image = models.URLField(blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    is_permanent = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("exhibition_detail", args=[self.pk])


class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ("Tour", "Tour"),
        ("Workshop", "Workshop"),
        ("Talk", "Talk"),
        ("Lecture", "Lecture"),
        ("Family", "Family"),
        ("Other", "Other"),
    ]

    title = models.CharField(max_length=200)
    event_type = models.CharField(
        max_length=50,
        choices=EVENT_TYPE_CHOICES,
        default="Other"
    )

    description = models.TextField()

    image = models.URLField(blank=True)

    date = models.DateField()
    time = models.TimeField()

    location = models.CharField(max_length=200)

    capacity = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date", "time"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event_detail", args=[self.pk])


class Booking(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("used", "Used"),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    ticket_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    number_of_tickets = models.PositiveIntegerField(default=1)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    booked_at = models.DateTimeField(auto_now_add=True)


class Visit(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("used", "Used"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="visits"
    )
    ticket_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    date = models.DateField()
    time = models.TimeField()
    number_of_visitors = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-booked_at"]

    def __str__(self):
        return (
            f"{self.user} - "
            f"{self.date} - "
            f"{self.number_of_visitors} visitors"
        )
