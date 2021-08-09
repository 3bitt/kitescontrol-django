from django import forms
from .models import Lesson
from account.models import User


class LessonCreateForm(forms.ModelForm):

    class Meta:
        model = Lesson
        exclude = [
            'creation_date',
            'paid',
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
            'comment',
            'confirmed',
            'in_progress',
            'completed'
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
                'step': '0.25'
            }),
            'confirmed': forms.CheckboxInput(),
            'in_progress': forms.CheckboxInput(),
            'completed': forms.CheckboxInput(),
            'kite_brand': forms.TextInput(attrs={
                'placeholder': 'Sygnatura kajta'
            }),
            'board': forms.TextInput(attrs={
                'placeholder': 'Sygnatura deski'
            }),
            'comment': forms.Textarea(attrs={
                'cols': 26,
                'rows': 3,
                'placeholder': 'Dodatkowe informacje'
            }),
            'instructor': forms.CheckboxSelectMultiple(),
            'student': forms.CheckboxSelectMultiple()

        }

        help_texts = {
            'start_time': "min. 7:00 - max. 21:00"
        }
