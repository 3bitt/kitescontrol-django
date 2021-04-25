from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING

from instructor.instructor.models import Instructor
from student.models import Student


class Lesson(models.Model):

    creation_date = models.DateTimeField(auto_now=True)
    start_date = models.DateField(null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
    student = models.ManyToManyField(Student, related_name='lessons')
    instructor = models.ManyToManyField(Instructor, related_name='lessons')
    group_lesson = models.BooleanField(null=True, blank=True)
    duration = models.FloatField(null=False, blank=False)
    paid = models.BooleanField(default=False, null=True, blank=True)
    # status not used yet
    status = models.CharField(max_length=30, default='0', null=True, blank=True)
    equipment = models.CharField(max_length=30, null=True, blank=True)
    kite_brand = models.CharField(max_length=30, null=True, blank=True)
    # kite_size not used yet
    kite_size = models.FloatField(null=True, blank=True)
    board = models.CharField(max_length=30, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    confirmed = models.BooleanField(default=False, null=True,blank=True)
    in_progress = models.BooleanField(default=False, null=True, blank=True)
    completed = models.BooleanField(default=False, null=True, blank=True)

    # Func used in template
    def get_start_time_class(self):
        hour = str(self.start_time.hour)

        # Return string which will be used in template as class
        # to determine lesson tile offset (position) in timetable
        if 0 < self.start_time.minute <= 15:
            return 'H' + hour + '-Q1'
        elif 15 < self.start_time.minute < 45:
            return 'H' + hour + '-Q2'
        elif self.start_time.minute >= 45:
            return 'H' + hour + '-Q3'
        else:
            return 'H' + hour

    # Func used in template - determine lesson tile span in timetable
    def get_column_span(self):
        return int(self.duration * 4)

    def i_dont_wanna_js(self):
        if (self.start_time.hour >= 20) or \
            (self.start_time.hour >= 19 and self.duration >= 2.5) or \
            (self.start_time.hour >= 18 and self.duration > 3):
            return True
        else:
            return False

    def get_date_formatted(self):
        return self.start_date.strftime('%d-%m-%Y')


class LessonDetail(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=CASCADE)
    student = models.ForeignKey(Student, on_delete=DO_NOTHING)
    duration = models.FloatField(null=True, blank=True)
    pay_rate = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    iko_level_achieved = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        unique_together = ['lesson', 'student']

    def __str__(self):
        return f'Detail_ID: {self.id}'
