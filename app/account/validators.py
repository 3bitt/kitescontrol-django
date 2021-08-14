import re
from datetime import datetime

from django.core.exceptions import ValidationError


def validate_name(value):
    if not value.isalpha():
        raise ValidationError('Only letters are allowed')
    return value


def validate_mobile(value):
    regexp = r'^(\+\d{1,3}[- ]?)?\d{9}$'
    if not re.match(regexp, value):
        raise ValidationError(
            'Number must have 9 digits and optionally country code (+00)'
        )
    return value


def validate_weight(value):
    if value < 0:
        raise ValidationError('Weight can\'t be negative!')
    return value


def validate_available_from(value):
    return value  # TODO
    # available_from = datetime.date(datetime.now())
    # available_from = value
    # return value


def validate_available_to(value):
    available_from = datetime.date(datetime.now())
    if value < available_from:
        raise ValidationError('Leave date can\'t be less than arrival date')
    return value
