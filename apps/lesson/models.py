from django.db import models

from instructor.instructor.models import Instructor
from student.models import Student

# Create your models here.


class Lesson(models.Model):
    creation_date = models.DateTimeField(auto_now=True)
    start_date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    student = models.ManyToManyField(Student, related_name='lessons')
    instructor = models.ManyToManyField(Instructor, related_name='lessons')
    duration = models.FloatField()
    paid = models.BooleanField(default=False, null=True, blank=True)
    status = models.CharField(max_length=30, null=True, blank=True)
    equipment = models.CharField(max_length=30, null=True, blank=True)
    kite_brand = models.CharField(max_length=30, null=True, blank=True)
    kite_size = models.FloatField(null=True, blank=True)
    board = models.CharField(max_length=30, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    in_progress = models.BooleanField(default=False, null=True, blank=True)
