from django import forms
from .models import Rental


class RentalCreateForm(forms.ModelForm):
    class Meta:
        model = Rental
        exclude = [
            'creation_date',
            'paid',
        ]

        fields = ['start_date', 'end_date', 'student', 'comment']
        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={'class': 'input', 'type': 'datetime-local'}
            ),
            'end_date': forms.DateTimeInput(
                attrs={'class': 'input', 'type': 'datetime-local'}
            ),
            'student': forms.RadioSelect(attrs={'class': 'input students-list'}),
            'comment': forms.TextInput(
                attrs={'class': 'input', 'type': 'text', 'max_length': 255}
            ),
        }


class RentalUpdateForm(forms.ModelForm):
    class Meta:
        model = Rental
        exclude = [
            'creation_date',
        ]

        fields = ['start_date', 'end_date', 'student', 'paid', 'comment']
        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={'class': 'input', 'type': 'datetime-local'}
            ),
            'end_date': forms.DateTimeInput(
                attrs={'class': 'input', 'type': 'datetime-local'}
            ),
            'student': forms.RadioSelect(attrs={'class': 'input students-list'}),
            'paid': forms.CheckboxInput(attrs={'class': 'input', 'type': 'checkbox'}),
            'comment': forms.TextInput(
                attrs={'class': 'input', 'type': 'text', 'max_length': 255}
            ),
        }

    def __init__(self, *args, **kwargs):
        rental_start_date = kwargs.get('instance').__getattribute__('start_date')
        rental_end_date = kwargs.get('instance').__getattribute__('end_date')

        start_date_converted = (
            rental_start_date.astimezone().strftime('%Y-%m-%dT%H:%M:%S')
            if rental_start_date
            else None
        )
        end_date_converted = (
            rental_end_date.astimezone().strftime('%Y-%m-%dT%H:%M:%S')
            if rental_end_date
            else None
        )

        kwargs.update(
            initial={'start_date': start_date_converted, 'end_date': end_date_converted}
        )
        super(RentalUpdateForm, self).__init__(*args, **kwargs)
