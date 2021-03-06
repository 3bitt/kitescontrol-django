from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.db.models import Q
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
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

# LESSON STATUSES:
# 0 - CREATED
# 1 - CONFIRMED
# 2 - COMPLETED

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

class LessonUpdateView(UpdateView):
    model = Lesson
    template_name = 'lesson/lesson_edit.html'
    form_class = LessonCreateForm

    def get_success_url(self):
        return reverse_lazy('lesson:lesson-list')

class LessonSetInProgressView(View):

    def post(self, request, **kwargs):
        lesson_id = self.kwargs['pk']
        lesson = Lesson.objects.get(id=lesson_id)
        if (lesson.in_progress):
            lesson.in_progress = False
            lesson.save()
        elif (not lesson.in_progress):
            lesson.in_progress = True
            lesson.save()
        else:
            lesson.in_progress = False
            lesson.save()
        return redirect('lesson:lesson-list')

class LessonConfirmView(View):
    def post(self,request, **kwargs):
        lesson_id = self.kwargs['pk']
        lesson = Lesson.objects.get(id=lesson_id)

        # LESSON STATUSES:
        # 0 - CREATED
        # 1 - CONFIRMED
        # 2 - COMPLETED
        if (lesson.status == '1'):
            lesson.status = '0'
            lesson.save()
        elif (lesson.status == '0'):
            lesson.status = '1'
            lesson.save()
        else:
            pass
        return redirect('lesson:lesson-list')

class LessonCompleteView(View):
    def post(self, request, **kwargs):
        lesson_id = self.kwargs['pk']
        lesson: Lesson = Lesson.objects.get(id=lesson_id)
        request_dict = self.request.POST

        for key in request_dict:
            if key.startswith('new_iko_level'):
                student_id = key.split('_')[-1]
                for student in lesson.student.all():
                    print(type(student.id))
                    print(type(student_id))
                    if student.id == int(student_id):
                        student.iko_level = request_dict[key]
                        student.save()

        lesson.completed = True
        lesson.status = '2'
        lesson.save()
        return redirect('lesson:lesson-list')


class LessonDeleteView(DeleteView):
    model = Lesson
    success_url = reverse_lazy('lesson:lesson-list')
