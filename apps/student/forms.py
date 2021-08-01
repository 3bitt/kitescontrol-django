from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from .models import Student



class StudentCreateForm(ModelForm):

    class Meta:
        model = Student
        exclude = ['lesson_hours_sum', 'register_date']

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
            'weight': forms.NumberInput(attrs = {
                'class': 'input',
                'type': 'number'
            }),
            'wetsuit_size': forms.Select(attrs= {
                'class': 'input',
                'choices': Student.WETSUIT_SIZES
            }),
            'harness_size': forms.Select(attrs= {
                'class': 'input',
                'choices': Student.HARNESS_SIZES
            }),
            'arrival_date': forms.DateInput(attrs = {
                'class': 'input',
                'type': 'date'
            }),
            'leave_date': forms.DateInput(attrs = {
                'class': 'input',
                'type': 'date'
            }),
            'email_address': forms.EmailInput(attrs = {
                'class': 'input',
                'type': 'email'
            }),
            'mobile_number': forms.NumberInput(attrs = {
                'class': 'input',
                'type': 'text',
                'placeholder': '+48 123456789'
            }),
            'stay_location': forms.TextInput(attrs = {
                'class': 'input',
                'type': 'text',
                'style': 'width: 154px;'
            }),
            'own_car': forms.CheckboxInput(attrs = {
                'class': 'input',
                'type': 'checkbox'
            }),
            'kite_elsewhere': forms.CheckboxInput(attrs = {
                'class': 'input',
                'type': 'checkbox'
            }),
            'iko_id': forms.NumberInput(attrs = {
                'class': 'input',
                'type': 'number'
            }),
            'iko_level': forms.Select(attrs={
                'class': 'input',
                'choices': Student.IKO_LEVELS
            }),
            'comment': forms.Textarea(attrs = {
                'class': 'input',
                'rows': 3,
                'cols': 23
            }),
            'pay_rate_single': forms.NumberInput(attrs = {
                'class': 'input short-field',
                'type': 'number'
            }),
            'pay_rate_group': forms.NumberInput(attrs = {
                'class': 'input short-field',
                'type': 'number'
            })
        }

        help_texts = {
            'mobile_number': "minimum 9 cyfr"
        }

    def clean(self):
        cleaned_data = super().clean()
        arrival_date = cleaned_data.get('arrival_date')
        leave_date = cleaned_data.get('leave_date')
        if arrival_date and leave_date and leave_date < arrival_date:
            raise ValidationError(
                {'leave_date': "Odjeżdza wcześniej niż przyjechał ? Chyba nie..."})

