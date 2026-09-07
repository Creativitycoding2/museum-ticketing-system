from django.db import models
from django.urls import reverse


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

