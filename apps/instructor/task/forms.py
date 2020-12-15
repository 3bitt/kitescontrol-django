from django.forms import ModelForm
from django import forms
from .models import Task

class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields =[
            'title',
            'description',
            'instructor',
            'value',
            'deadline_date',
            'completed_flag']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input form-control',
                'type': 'text'
            }),
            'description': forms.Textarea(attrs = {
                'class': 'input form-control',
                'rows': 3,
                'cols': 23
            }),
            # 'instructor': forms.CheckboxSelectMultiple(),
            'value': forms.NumberInput(attrs={
                'class': 'input form-control',
                'type': 'number'
            }),
            'deadline_date': forms.DateInput(attrs={
                'class': 'input form-control',
                'type': 'date'
            }),
            'completed_flag': forms.CheckboxInput(attrs={
                'class': 'input ',
                'type': 'checkbox'
            })
        }