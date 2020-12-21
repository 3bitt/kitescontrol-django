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
            'kite_brand',
            'kite_size',
            'board'
            ]
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date'
            })
        }
