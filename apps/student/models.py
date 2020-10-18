from django.db import models
from django.urls import reverse

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    surname = models.CharField(max_length=30, null=False, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    wetsuit_size = models.CharField(max_length=3, null=True, blank=True)
    harness_size = models.CharField(max_length=3, null=True, blank=True)
    arrival_date = models.DateField(null=True, blank=True)
    leave_date = models.DateField(null=True, blank=True)
    email_address = models.CharField(max_length=40, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
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
    
