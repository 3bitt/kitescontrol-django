from django.forms import ModelForm
from django import forms
from .models import Lesson
from account.models import User

class LessonCreateForm(forms.ModelForm):

    class Meta:
        model = Lesson
        exclude = [
            'creation_date',
            'paid',
            'in_progress',
            'kite_size',
            'start_time',

            ]
        fields = [
            'start_date',
            'student',
            'instructor',
            'duration',
            'status',
            'equipment',
            'kite_brand',
            'board',
            'comment'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'input',
                'min': '0.5',
                'max': '6',
                'step': '0.5'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'input',
                'type': 'time',
                'step': '900',
                'min': '07:00',
                'max': '21:00',
                'required': False
            }),
            'instructor': forms.CheckboxSelectMultiple,
            'student': forms.CheckboxSelectMultiple

        }

        help_texts = {
            'start_time': "min. 7:00 - max. 21:00"
        }