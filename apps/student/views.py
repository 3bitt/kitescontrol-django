from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from .forms import StudentCreateForm
from .models import Student

class StudentListView(ListView):

    queryset = Student.objects.all().order_by('-register_date')
    context_object_name = 'students'
    # model = Student
    template_name = 'student/student_list.html'


class StudentCreateView(CreateView):
    model = Student
    template_name = 'student/student_create.html'
    # fields = '__all__'
    form_class = StudentCreateForm
    # success_url = ''


class StudentDetailView(DetailView):
    # queryset = Student.objects.all()
    template_name = 'student/student_detail.html'
    context_object_name = 'student'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Student, id=id_)