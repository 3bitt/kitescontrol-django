from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.db.models import Q
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from instructor.instructor.models import Instructor
from student.models import Student
from .models import Lesson, LessonDetail
import pytz
from datetime import date, datetime, timedelta
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
    # context_object_name = 'instructors_all'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if (self.kwargs):
            self.current_date = self.kwargs['schedule_date']

        lessons_today = Lesson.objects.filter(start_date=self.current_date).order_by('start_time')
        context['instructors_with_lessons'] = self.queryset.prefetch_related(
            Prefetch('lessons', lessons_today)
        )

        context['hours'] = range(7,22)
        context['current_date'] = self.current_date
        context['current_time'] = datetime.today().hour

        context['previous_date'] = self.current_date - timedelta(days=1)
        context['next_date'] = datetime.date(self.current_date + timedelta(days=1))

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

    def form_valid(self, form: LessonCreateForm):
        start_hour = int(self.request.POST['start_hour'])
        start_minute = int(self.request.POST['start_minute'])
        start_time = datetimeModule.time(start_hour,start_minute)
        form.instance.start_time = start_time

        if len(form.cleaned_data['student']) > 1:
            form.instance.group_lesson = True
        else:
            form.instance.group_lesson = False

        if form.cleaned_data['start_date'] != datetime.date(self.current_date):
            lesson_date = form.cleaned_data['start_date'].strftime('%d-%m-%Y')
            self.success_url = reverse_lazy('lesson:lesson-list', kwargs={'schedule_date': lesson_date})

        response = super(LessonCreateView, self).form_valid(form)

        # return super().form_valid(form)
        return response

class LessonUpdateView(UpdateView):
    current_date = datetime.today()
    model = Lesson
    template_name = 'lesson/lesson_edit.html'
    form_class = LessonCreateForm
    success_url = reverse_lazy('lesson:lesson-list')

    def form_valid(self, form: LessonCreateForm):
        if form.cleaned_data['start_date'] != datetime.date(self.current_date):
            lesson_date = form.cleaned_data['start_date'].strftime('%d-%m-%Y')
            self.success_url = reverse_lazy('lesson:lesson-list', kwargs={'schedule_date': lesson_date})

        response = super(LessonUpdateView, self).form_valid(form)

        # return super().form_valid(form)
        return response

    # def get_success_url(self):
    #     return reverse_lazy('lesson:lesson-list')

class LessonStartView(View):

    def post(self, request, **kwargs):
        lesson_id = self.kwargs['pk']
        lesson = Lesson.objects.get(id=lesson_id)
        if (lesson.in_progress):
            lesson.in_progress = False
            lesson.confirmed = False
        elif (not lesson.in_progress):
            lesson.in_progress = True
            lesson.confirmed = True
        else:
            lesson.in_progress = False
            lesson.confirmed = False
        lesson.save()
        return redirect('lesson:lesson-list')

class LessonConfirmView(View):
    def post(self,request, **kwargs):
        lesson_id = self.kwargs['pk']
        lesson: Lesson = Lesson.objects.get(id=lesson_id)

        # LESSON STATUSES:
        # 0 - CREATED
        # 1 - CONFIRMED
        # 2 - COMPLETED
        if (lesson.confirmed ):
            lesson.confirmed = False
        elif (not lesson.confirmed):
            lesson.confirmed = True
        else:
            pass
        lesson.save()
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
                    if student.id == int(student_id):
                        student.iko_level = request_dict[key]
                        student.save()

                        if lesson.group_lesson:
                            pay_rate = student.pay_rate_group
                        else:
                            pay_rate = student.pay_rate_single

                        student_lesson_time = float(request_dict[f'student_lesson_duration_{student_id}'])

                        lesson_detail_object, created = LessonDetail.objects.update_or_create(
                            lesson=lesson, student=student,
                            defaults = {
                                'lesson': lesson,
                                'student': student,
                                'duration': student_lesson_time,
                                'pay_rate': int(pay_rate),
                                'price': int(pay_rate) * student_lesson_time,
                                'iko_level_achieved': request_dict[key]
                            }
                        )

        lesson.duration = request_dict['duration']
        lesson.completed = True
        lesson.in_progress = False
        lesson.save()
        return redirect('lesson:lesson-list')


class LessonDeleteView(DeleteView):
    model = Lesson
    success_url = reverse_lazy('lesson:lesson-list')


class FindScheduleRedirectView(View):
    http_method_names = ['get']
    def get(self, request):
        request_date = request.GET['schedule_date']
        request_date_clean = datetime.strptime(request_date, '%Y-%m-%d').strftime('%d-%m-%Y')
        return redirect('lesson:lesson-list', request_date_clean)
