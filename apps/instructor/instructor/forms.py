from django.forms import ModelForm, SelectDateWidget
from django import forms
from .models import Instructor

class InstructorCreateForm(ModelForm):
    class Meta:
        model = Instructor
        exclude = [
            'tc_accepted_date',
            'active',
            'register_date'
            ]

        widgets = {
            'name': forms.TextInput(attrs = {
                'class': 'input'
            }),
            'surname': forms.TextInput(attrs = {
                'class': 'input'
            }),
            'birth_date': forms.DateInput(attrs = {
                'class': 'input',
                'type': 'date'
            }),
            'mobile_number': forms.NumberInput(attrs = {
                'class': 'input',
                'type': 'text',
                'placeholder': '+48 123456789'
            }),
            'email_address': forms.EmailInput(attrs = {
                'class': 'input',
                'type': 'email'
            }),
            'weight': forms.NumberInput(attrs = {
                'class': 'input',
                'type': 'number'
            }),
            'available_from': forms.DateInput(attrs = {
                'class': 'input',
                'type': 'date'
            }),
            'available_to': forms.DateInput(attrs = {
                'class': 'input',
                'type': 'date'
            }),
            'iko_id': forms.NumberInput(attrs = {
                'class': 'input',
                'type': 'number'
            }),
            'iko_level': forms.Select(attrs = {
                'class': 'input',
                'choices': Instructor.IKO_LEVELS
            }),
            'driving_licence': forms.CheckboxInput(attrs = {
                'class': 'input',
                'type': 'checkbox'
            }),
            'pay_rate_single': forms.NumberInput(attrs = {
                'class': 'input',
                'type': 'number'
            }),
            'pay_rate_group': forms.NumberInput(attrs = {
                'class': 'input',
                'type': 'number'
            }),
            'english_lessons': forms.CheckboxInput(attrs = {
                'class': 'input',
                'type': 'checkbox'
            }),
            'kids_lessons': forms.CheckboxInput(attrs = {
                'class': 'input',
                'type': 'checkbox'
            }),
            'group_lessons': forms.CheckboxInput(attrs = {
                'class': 'input',
                'type': 'checkbox'
            }),
            'daily_hour_limit': forms.NumberInput(attrs = {
                'class': 'input',
                'type': 'number'
            }),
            'tc_accepted_flag': forms.CheckboxInput(attrs = {
                'class': 'input',
                'type': 'checkbox'
            }),
        }

        help_texts = {
            'mobile_number': "minimum 9 cyfr"
        }