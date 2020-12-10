from django.db import models
from django.urls import reverse
from .validators import (
    validate_name,
    validate_mobile,
    validate_weight,
    validate_available_from,
    validate_available_to
)

# Create your models here.


class Instructor(models.Model):

    IKO_LEVELS = (
        (None, 'Brak'),
        ('Asystent', 'Asystent'),
        ('Instruktor 1', 'Instruktor 1'),
        ('Instruktor 2', 'Instruktor 2'),
        ('Insturktor 3', 'Instruktor 3'),
        ('Coach', 'Coach'),
    )

    name = models.CharField(max_length=30, null=False, blank=False, validators=[validate_name])
    surname = models.CharField(max_length=30, null=False, blank=False, validators=[validate_name])
    nickname = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=False, blank=False)
    mobile_number = models.CharField(max_length=20, null=True, blank=True, validators=[validate_mobile])
    email_address = models.CharField(max_length=40, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True, validators=[validate_weight])
    available_from = models.DateField(null=True, blank=True, validators=[validate_available_from])
    available_to = models.DateField(null=True, blank=True, validators=[validate_available_to])
    iko_id = models.IntegerField(null=True, blank=True)
    iko_level = models.CharField(max_length=30, null=True, blank=True, choices=IKO_LEVELS)
    driving_licence = models.BooleanField(null=True, default=False)
    pay_rate_single = models.IntegerField(null=True, blank=True)
    pay_rate_group = models.IntegerField(null=True, blank=True)
    english_lessons = models.BooleanField(null=True, blank=True, default=False)
    kids_lessons = models.BooleanField(null=True, blank=True, default=False)
    group_lessons = models.BooleanField(null=True, blank=True, default=False)
    daily_hour_limit = models.IntegerField(null=True, blank=True)
    tc_accepted_date = models.DateField(null=True, blank=True)
    tc_accepted_flag = models.BooleanField(null=True, default=False)
    active = models.BooleanField(blank=True, default=True)
    register_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_absolute_url(self):
        return reverse("instructor:instructor-detail", kwargs={"pk": self.pk})
