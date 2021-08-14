from django.forms import ModelForm
from django import forms
from .models import Instructor
from account.models import User


class InstructorCreateForm(ModelForm):
    class Meta:
        model = Instructor
        exclude = ['tc_accepted_date', 'active', 'weight', 'register_date']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'surname': forms.TextInput(attrs={'class': 'input'}),
            'birth_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'mobile_number': forms.NumberInput(
                attrs={'class': 'input', 'type': 'text', 'placeholder': '+48 123456789'}
            ),
            'email_address': forms.EmailInput(attrs={'class': 'input', 'type': 'email'}),
            'available_from': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'available_to': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'iko_id': forms.NumberInput(attrs={'class': 'input', 'type': 'number'}),
            'iko_level': forms.Select(
                attrs={'class': 'input', 'choices': Instructor.IKO_LEVELS}
            ),
            'driving_licence': forms.CheckboxInput(
                attrs={'class': 'input', 'type': 'checkbox'}
            ),
            'pay_rate_single': forms.NumberInput(
                attrs={'class': 'input', 'type': 'number'}
            ),
            'pay_rate_group': forms.NumberInput(
                attrs={'class': 'input', 'type': 'number'}
            ),
            'english_lessons': forms.CheckboxInput(
                attrs={'class': 'input', 'type': 'checkbox'}
            ),
            'kids_lessons': forms.CheckboxInput(
                attrs={'class': 'input', 'type': 'checkbox'}
            ),
            'group_lessons': forms.CheckboxInput(
                attrs={'class': 'input', 'type': 'checkbox'}
            ),
            'daily_hour_limit': forms.NumberInput(
                attrs={'class': 'input', 'type': 'number'}
            ),
            'tc_accepted_flag': forms.CheckboxInput(
                attrs={'class': 'input', 'type': 'checkbox'}
            ),
        }

        help_texts = {'mobile_number': "minimum 9 cyfr"}

    def save(self, userType, commit=True):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate."
                % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save(userType)
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        return self.instance


class InstructorEditForm(ModelForm):
    class Meta:
        model = Instructor
        exclude = ['tc_accepted_date', 'register_date', 'weight', 'user']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'surname': forms.TextInput(attrs={'class': 'input'}),
            'birth_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'mobile_number': forms.NumberInput(
                attrs={'class': 'input', 'type': 'text', 'placeholder': '+48 123456789'}
            ),
            'email_address': forms.EmailInput(attrs={'class': 'input', 'type': 'email'}),
            'available_from': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'available_to': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'iko_id': forms.NumberInput(attrs={'class': 'input', 'type': 'number'}),
            'iko_level': forms.Select(
                attrs={'class': 'input', 'choices': Instructor.IKO_LEVELS}
            ),
            'driving_licence': forms.CheckboxInput(
                attrs={'class': 'input', 'type': 'checkbox'}
            ),
            'pay_rate_single': forms.NumberInput(
                attrs={'class': 'input', 'type': 'number'}
            ),
            'pay_rate_group': forms.NumberInput(
                attrs={'class': 'input', 'type': 'number'}
            ),
            'english_lessons': forms.CheckboxInput(
                attrs={'class': 'input', 'type': 'checkbox'}
            ),
            'kids_lessons': forms.CheckboxInput(
                attrs={'class': 'input', 'type': 'checkbox'}
            ),
            'group_lessons': forms.CheckboxInput(
                attrs={'class': 'input', 'type': 'checkbox'}
            ),
            'daily_hour_limit': forms.NumberInput(
                attrs={'class': 'input', 'type': 'number'}
            ),
            'tc_accepted_flag': forms.CheckboxInput(
                attrs={'class': 'input', 'type': 'checkbox'}
            ),
            'active': forms.CheckboxInput(attrs={'class': 'input', 'type': 'checkbox'}),
        }

        help_texts = {'mobile_number': "minimum 9 cyfr"}

    def save(self, userType=None, commit=True):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate."
                % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save(userType)
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        return self.instance
