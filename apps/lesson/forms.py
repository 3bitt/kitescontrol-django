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
                'step': '0.5'
            }),
            'confirmed': forms.CheckboxInput(),
            'in_progress': forms.CheckboxInput(),
            'completed': forms.CheckboxInput(),
            'instructor': forms.CheckboxSelectMultiple,
            'student': forms.CheckboxSelectMultiple

        }

        help_texts = {
            'start_time': "min. 7:00 - max. 21:00"
        }

    def __init__(self, *args, **kwargs):
        # lesson_start_time = kwargs.get(
        #     'instance').__getattribute__(
        #         'start_time')
        # lesson_start_time = lesson_start_time.strftime('%H:%S').split(':')
        # print(lesson_start_time)

        # kwargs.update(initial = {
        #     'start_hour' : lesson_start_time[0],
        #     'start_minute' : lesson_start_time[1],
        # })
        super(LessonCreateForm, self).__init__(*args, **kwargs)
