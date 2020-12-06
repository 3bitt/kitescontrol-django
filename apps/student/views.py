from django.views.generic import CreateView, ListView, DetailView, DeleteView,UpdateView
from django.shortcuts import get_object_or_404
from .forms import StudentCreateForm
from .models import Student
from django.urls import reverse_lazy
from django.db.models import Q
from django.db.models.functions import Trim

class StudentListView(ListView):

    queryset = Student.objects.all().order_by('-register_date')[:30]
    context_object_name = 'student_list'
    # model = Student
    template_name = 'student/student_list.html'

class StudentSearchView(ListView):

    context_object_name = 'student_list'
    template_name = 'student/student_list.html'

    # Queryset using query params in search
    def get_queryset(self):
        q = Student.objects.filter(
            Q(mobile_number__contains=self.request.GET['s_mobile']),
            Q(name__contains=self.request.GET['s_name']) |
            Q(surname__contains=self.request.GET['s_name'])
            ).order_by('-register_date')
        return q

    # Populate context with user input so template can display it in search fields
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mobile_num_user_input'] = self.request.GET['s_mobile']
        context['student_name_user_input'] = self.request.GET['s_name']
        return context

class StudentCreateView(CreateView):
    model = Student
    template_name = 'student/student_create.html'
    # fields = '__all__'
    form_class = StudentCreateForm
    success_url = reverse_lazy('student:student-list')


class StudentDetailView(DetailView):
    queryset = Student.objects.all()
    template_name = 'student/student_detail.html'
    context_object_name = 'student'

    editMode = False


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'student/student_detail.html'
    editMode = False
    form_class = StudentCreateForm

    def get_success_url(self):
        return reverse_lazy('student:student-detail', kwargs={'pk': self.kwargs['pk']})

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student/student_delete.html'
    success_url = reverse_lazy('student:student-list')