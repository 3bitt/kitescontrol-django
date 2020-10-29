from django.db import models
from django.urls import reverse
from .validators import validate_name, validate_mobile




class Student(models.Model):

    WETSUIT_SIZES = (
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL')
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
    weight = models.FloatField(null=True, blank=True)
    wetsuit_size = models.CharField(
        max_length=3, 
        null=True, 
        blank=True, 
        choices=WETSUIT_SIZES)
    harness_size = models.CharField(
        max_length=3, 
        null=True, 
        blank=True, 
        choices=HARNESS_SIZES)
    arrival_date = models.DateField(null=True, blank=True)
    leave_date = models.DateField(null=True, blank=True)
    email_address = models.CharField(max_length=40, null=True, blank=True)
    mobile_number = models.CharField(
        max_length=20, 
        null=True, 
        blank=False,
        validators=[validate_mobile])
    stay_location = models.CharField(max_length=40, null=True, blank=True)
    iko_id = models.IntegerField(null=True, blank=True)
    iko_level = models.CharField(max_length=30, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    register_date = models.DateTimeField(auto_now_add=True)
    # https://stackoverflow.com/questions/34275588/djangorestframework-modelserializer-datetimefield-only-converting-to-current-tim

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_absolute_url(self):
        return reverse("student:student-detail", kwargs={"id": self.pk})
    
