from django.core.exceptions import ValidationError
import re
from datetime import datetime

def validate_name(value):
    if not value.isalpha():
        raise ValidationError('Only letters are allowed')
    return value

def validate_mobile(value):
    regexp = r'^(\+\d{1,3}[- ]?)?\d{9}$'
    if not re.match(regexp, value):
        raise ValidationError('Number must have 9 digits and optionally country code (+00)')
    return value

def validate_weight(value):
  if value < 0:
    raise ValidationError('Weight can\'t be negative!)')
  return value


arrival_date = datetime.date(datetime.now())

def validate_arrival_date(value):
  arrival_date = value
  return value

def validate_leave_date(value):
  if value < arrival_date:
    raise ValidationError('Leave date can\'t be less than arrival date')
  return value
