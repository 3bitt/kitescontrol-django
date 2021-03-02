from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.db.models import Q
from instructor.instructor.models import Instructor
from student.models import Student
from .models import Lesson
import pytz
from datetime import date, datetime
import datetime as datetimeModule
from .forms import LessonCreateForm
from django.urls import reverse_lazy
from django.core import serializers
import json

from django.core.serializers import serialize
from django.db.models import OuterRef, Subquery
from django.db.models import Prefetch

class LessonListView(ListView):
    current_date = datetime.today()
    # current_date = date.today()
    queryset = Instructor.objects.filter(active=True)
    template_name = 'lesson/lesson_list.html'
    context_object_name = 'instructors_all'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_lessons = Lesson.objects.filter(start_date=self.current_date).order_by('start_time')
        context['instructors_with_lessons'] = self.queryset.prefetch_related(
            Prefetch('lessons', today_lessons)
        )
        context['hours'] = range(7,22)
        context['current_date'] = self.current_date
        context['current_time'] = datetime.today().hour

        return context


class LessonCreateView(CreateView):
    current_date = datetime.today()
    model = Lesson
    template_name = 'lesson/lesson_create.html'
    form_class = LessonCreateForm
    success_url = reverse_lazy('lesson:lesson-list')

    students_query = Student.objects.filter(
            Q(arrival_date__lte=current_date),
            Q(leave_date__gte=current_date)
        ).order_by('-register_date', '-name')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)  # Get the form as usual
        form.fields['instructor'].queryset = Instructor.objects.filter(active=True).order_by('-register_date', '-name')
        form.fields['student'].queryset = self.students_query
        form.fields['duration'].initial = 2
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students_query"] = serialize('json',
            self.students_query,
            )
        return context

    # def get_form_kwargs(self):
    #     form = super(LessonCreateView, self).get_form_kwargs()
    #     form['duration'] = 2
    #     return super().get_form_kwargs()

    def form_valid(self, form: LessonCreateForm):
        start_hour = int(self.request.POST['start_hour'])
        start_minute = int(self.request.POST['start_minute'])
        start_time = datetimeModule.time(start_hour,start_minute)
        form.instance.start_time = start_time
        return super().form_valid(form)


class LessonDeleteView(DeleteView):
    model = Lesson
    success_url = reverse_lazy('lesson:lesson-list')
