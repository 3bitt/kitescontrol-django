from django import forms
from django.forms.fields import SplitDateTimeField
from django.forms.widgets import MultiWidget, SplitDateTimeWidget
from .models import Rental, RentalDetail
from student.models import Student

class RentalCreateForm(forms.ModelForm):
    class Meta:
        model = Rental
        exclude = [
            'creation_date',
            'paid',
            ]

        fields = [
            'start_date',
            'end_date',
            'student',
            'comment'
        ]
        widgets = {
            'start_date': forms.DateTimeInput(attrs={
                'class': 'input',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'input',
                'type': 'datetime-local'
            }),
            'student': forms.RadioSelect(attrs={
                'class': 'input students-list'
            }),
            'comment': forms.TextInput(attrs={
                'class': 'input',
                'type' : 'text',
                'max_length': 255
            }),

        }
