from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)
from django.views.generic.base import TemplateView

from .forms import InstructorCreateForm, InstructorEditForm
from .models import Instructor


class InstructorHomeView(TemplateView):
    template_name = 'instructor/instructor_home.html'


class InstructorListView(ListView):
    queryset = Instructor.objects.all().order_by('-register_date')
    context_object_name = 'instructor_list'
    template_name = 'instructor/instructor_list.html'


class InstructorCreateView(CreateView):
    model = Instructor
    template_name = 'instructor/instructor_create.html'
    form_class = InstructorCreateForm
    success_url = reverse_lazy('instructor:instructor-list')


class InstructorDetailView(DetailView):
    queryset = Instructor.objects.order_by('-register_date')
    template_name = 'instructor/instructor_detail.html'
    context_object_name = 'instructor'
    editMode = False


class InstructorUpdateView(UpdateView):
    model = Instructor
    template_name = 'instructor/instructor_detail.html'
    editMode = False
    form_class = InstructorEditForm

    def get_success_url(self):
        return reverse_lazy('instructor:instructor-detail', kwargs={'pk': self.kwargs['pk']})


class InstructorDeleteView(DeleteView):
    model = Instructor
    success_url = reverse_lazy('instructor:instructor-list')
