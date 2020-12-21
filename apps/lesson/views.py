from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.db.models import Q
from instructor.instructor.models import Instructor
from .models import Lesson
from datetime import date
from .forms import LessonCreateForm
from django.urls import reverse_lazy

from django.core.serializers import serialize
from django.db.models import OuterRef, Subquery
from django.db.models import Prefetch

class LessonListView(ListView):
    current_date = date.today()
    queryset = Instructor.objects.all()
    template_name = 'lesson/lesson_list.html'
    context_object_name = 'instructors_all'
    print('CURR DATE: ', current_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_lessons = Lesson.objects.filter(start_date=self.current_date).order_by('start_time')

        context['instructors_with_lessons'] = self.queryset.prefetch_related(
            Prefetch('lessons', today_lessons)
        )
        context['hours'] = range(7,22)

        return context


class LessonCreateView(CreateView):
    model = Lesson
    template_name = 'lesson/lesson_create.html'
    form_class = LessonCreateForm
    success_url = reverse_lazy('lesson:lesson-list')

class LessonDeleteView(DeleteView):
    model = Lesson
    success_url = reverse_lazy('lesson:lesson-list')
