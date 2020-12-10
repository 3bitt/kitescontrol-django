from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Task
from .forms import TaskCreateForm
from django.urls import reverse_lazy

class TaskListView(ListView):
    queryset = Task.objects.all().order_by('-created_date')
    context_object_name = 'tasks'
    template_name = 'task/task_list.html'

class TaskCreateView(CreateView):
    model = Task
    template_name = 'task/task_create.html'
    form_class = TaskCreateForm
    success_url = reverse_lazy('task:task-list')

