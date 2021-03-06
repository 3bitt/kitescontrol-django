from django.db import models

from instructor.instructor.models import Instructor
from student.models import Student

# Create your models here.


# LESSON STATUSES:
# 0 - CREATED
# 1 - CONFIRMED
# 2 - COMPLETED

class Lesson(models.Model):

    creation_date = models.DateTimeField(auto_now=True)
    start_date = models.DateField(null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
    student = models.ManyToManyField(Student, related_name='lessons')
    instructor = models.ManyToManyField(Instructor, related_name='lessons')
    duration = models.FloatField(null=False, blank=False)
    paid = models.BooleanField(default=False, null=True, blank=True)
    status = models.CharField(max_length=30, default='0', null=True, blank=True)
    equipment = models.CharField(max_length=30, null=True, blank=True)
    kite_brand = models.CharField(max_length=30, null=True, blank=True)
    kite_size = models.FloatField(null=True, blank=True)
    board = models.CharField(max_length=30, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    in_progress = models.BooleanField(default=False, null=True, blank=True)
    completed = models.BooleanField(default=False, null=True, blank=True)

    # Func used in template
    def get_start_time_class(self):
        hour = str(self.start_time.hour)

        # Return string which will be used in template as class
        # to determine lesson tile offset (position) in timetable
        if 0 < self.start_time.minute <= 15:
            return "H" + hour + "-Q1"
        elif 15 < self.start_time.minute < 45:
            return "H" + hour + "-Q2"
        elif self.start_time.minute >= 45:
            return "H" + hour + "-Q3"
        else:
            return "H" + hour

    # Func used in template - determine lesson tile span in timetable
    def get_column_span(self):
        return int(self.duration * 4)
