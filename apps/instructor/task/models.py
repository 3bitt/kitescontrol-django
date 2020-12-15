from django.db import models
from instructor.instructor.models import Instructor
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=255, null=False)
    instructor = models.ManyToManyField(Instructor, related_name='task', related_query_name='task')
    value = models.FloatField(default=0)
    deadline_date = models.DateField(null=False)
    completed_date = models.DateField(null=True, blank=True)
    completed_flag = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
