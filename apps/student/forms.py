from django.forms import ModelForm, SelectDateWidget
from django import forms
from .models import Student

class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs = {
                'class': 'input'
            }),
            'surnamename': forms.TextInput(attrs = {
                'class': 'input'
            }),
            'birth_date': forms.DateInput,
            'email_address': forms.EmailInput(attrs = {
                'class': 'input'
            }),
        }

        help_texts = {
            'birth_date': ('format: YYYY-MM-DD')
        }