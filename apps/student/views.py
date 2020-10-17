from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Student


class ListStudentView(ListView):
    queryset = Student.objects.all().order_by('-register_date')
    context_object_name = 'students'
    # model = Student
    template_name = 'student/student_list.html'


class CreateStudentView(CreateView):
    model = Student
    template_name = 'student/student_create.html'
    fields = '__all__'
