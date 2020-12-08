from django.db import models

# Create your models here.


class Instructor(models.Model):

    name = models.CharField(max_length=30, null=False, blank=False)
    surname = models.CharField(max_length=30, null=False, blank=False)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=False, blank=False)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    email_address = models.CharField(max_length=40, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    available_from = models.DateField(null=True, blank=True)
    available_to = models.DateField(null=True, blank=True)
    iko_id = models.IntegerField(null=True, blank=True)
    iko_level = models.CharField(max_length=30, null=True, blank=True)
    pay_rate_single = models.IntegerField(null=True, blank=True)
    pay_rate_group = models.IntegerField(null=True, blank=True)
    english_lessons = models.BooleanField(null=True, blank=True)
    kids_lessons = models.BooleanField(null=True, blank=True)
    group_lessons = models.BooleanField(null=True, blank=True)
    daily_hour_limit = models.FloatField(null=True, blank=True)
    active = models.BooleanField(blank=True, default=True)

    def __str__(self):
        return f'{self.name} {self.surname}'
