from django.forms import ModelForm, SelectDateWidget
from django import forms
from .models import Student



class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

        # widgets = {
        #     'name': forms.TextInput(attrs = {
        #         'class': 'input'
        #     }),
        #     'surname': forms.TextInput(attrs = {
        #         'class': 'input'
        #     }),
        #     'birth_date': forms.DateInput(attrs = {
        #         'class': 'input',
        #         'type': 'date'
        #     }),
        #     'weight': forms.NumberInput(attrs = {
        #         'class': 'input',
        #         'type': 'number'
        #     }),
        #     'wetsuit_size': forms.Select(attrs= {
        #         'class': 'input',
        #         'choices': Student.WETSUIT_SIZES
        #     }),
        #     'harness_size': forms.Select(attrs= {
        #         'class': 'input',
        #         'choices': Student.HARNESS_SIZES
        #     }),
        #     'arrival_date': forms.DateInput(attrs = {
        #         'class': 'input',
        #         'type': 'date'
        #     }),
        #     'leave_date': forms.DateInput(attrs = {
        #         'class': 'input',
        #         'type': 'date'
        #     }),
        #     'email_address': forms.EmailInput(attrs = {
        #         'class': 'input',
        #     }),
        #     'mobile_number': forms.NumberInput(attrs = {
        #         'class': 'input',
        #         'type': 'text'
        #     }),
        #     'stay_location': forms.TextInput(attrs = {
        #         'class': 'input',
        #         'type': 'text'
        #     }),
        #     'iko_id': forms.NumberInput(attrs = {
        #         'class': 'input',
        #         'type': 'text'
        #     }),
        #     'iko_level': forms.NumberInput(attrs = {
        #         'class': 'input',
        #         'type': 'text',
        #     }),
        #     'comment': forms.TextInput(attrs = {
        #         'class': 'input',
        #         'type': 'text'
        #     }),
        # }

        # help_texts = {
        # }