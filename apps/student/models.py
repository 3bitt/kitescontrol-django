from django.db import models
from django.urls import reverse
from .validators import (
    validate_name,
    validate_mobile,
    validate_weight,
    validate_arrival_date,
    validate_leave_date,
)




class Student(models.Model):

    WETSUIT_SIZES = (
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('S-128', 'S-128'),
        ('M-140', 'M-140'),
        ('L-146', 'L-146'),
        ('XL-152', 'XL-152'),
    )
    HARNESS_SIZES = (
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL')
    )

    name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        validators=[validate_name])

    surname = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        validators=[validate_name])

    birth_date = models.DateField(null=True, blank=False)

    mobile_number = models.CharField(
        max_length=20,
        null=True,
        blank=False,
        unique=True,
        validators=[validate_mobile])

    email_address = models.CharField(max_length=40, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True, default=0, validators=[validate_weight])
    arrival_date = models.DateField(null=True, blank=True, validators=[validate_arrival_date])
    leave_date = models.DateField(null=True, blank=True, validators=[validate_leave_date])
    stay_location = models.CharField(max_length=40, null=True, blank=True)
    own_car = models.BooleanField(null=True,blank=True, default=False)
    kite_elsewhere = models.BooleanField(null=True,blank=True,default=False)

    wetsuit_size = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        choices=WETSUIT_SIZES)

    harness_size = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        choices=HARNESS_SIZES)

    iko_id = models.IntegerField(null=True, blank=True, unique=True)
    iko_level = models.CharField(max_length=30, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    pay_rate_single = models.IntegerField(null=False, blank=False)
    pay_rate_group = models.IntegerField(null=False, blank=False)
    register_date = models.DateTimeField(auto_now_add=True)
    # https://stackoverflow.com/questions/34275588/djangorestframework-modelserializer-datetimefield-only-converting-to-current-tim

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_absolute_url(self):
        return reverse("student:student-detail", kwargs={"pk": self.pk})
