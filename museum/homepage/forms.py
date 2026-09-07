from django import forms
from .models import Exhibition, Event


class ExhibitionForm(forms.ModelForm):
    class Meta:
        model = Exhibition
        fields = [
            "title",
            "category",
            "description",
            "image",
            "start_date",
            "end_date",
            "is_permanent",
            "is_active",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
            }),
            "category": forms.Select(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
                "rows": 5,
            }),
            "image": forms.URLInput(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
            }),
            "start_date": forms.DateInput(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
                "type": "date",
            }),
            "end_date": forms.DateInput(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
                "type": "date",
            }),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "event_type",
            "description",
            "image",
            "date",
            "time",
            "location",
            "capacity",
            "is_active",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
            }),

            "event_type": forms.Select(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
            }),

            "description": forms.Textarea(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
                "rows": 5,
            }),

            "image": forms.URLInput(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
            }),

            "date": forms.DateInput(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
                "type": "date",
            }),

            "time": forms.TimeInput(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
                "type": "time",
            }),

            "location": forms.TextInput(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
            }),

            "capacity": forms.NumberInput(attrs={
                "class": "w-full border border-stone-300 rounded-lg px-4 py-2",
                "min": 1,
            }),
        }
