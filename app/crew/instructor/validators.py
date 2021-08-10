import re
from django.core.exceptions import ValidationError
from datetime import datetime

def validate_name(value):
    if not value.isalpha():
        raise ValidationError('Only letters are allowed')
    return value

# def validate_email_address(value):
#     if User.objects.filter(email__iexact=value) is None:
#         raise ValidationError('This email already exists')
#     return value

def validate_mobile(value):
    regexp = r'^(\+\d{1,3}[- ]?)?\d{9}$'
    if not re.match(regexp, value):
        raise ValidationError('Number must have 9 digits and optionally country code (+00)')
    return value

def validate_weight(value):
    if value < 0:
        raise ValidationError('Weight can\'t be negative!')
    return value

available_from = datetime.date(datetime.now())

def validate_available_from(value):
    available_from = value
    return value

def validate_available_to(value):
    if value < available_from:
      raise ValidationError('Leave date can\'t be less than arrival date')
    return value
