from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Task
from .forms import TaskCreateForm
from django.urls import reverse_lazy
from datetime import date

class TaskListView(ListView):
    queryset = Task.objects.all().order_by('-created_date')
    context_object_name = 'tasks'
    template_name = 'task/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_date"] = date.today()
        context["tasks_dates"] = self.queryset.values_list('deadline_date',flat=True).distinct()
        return context



class TaskCreateView(CreateView):
    model = Task
    template_name = 'task/task_create.html'
    form_class = TaskCreateForm
    success_url = reverse_lazy('task:task-list')

