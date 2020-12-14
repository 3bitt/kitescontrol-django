from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
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

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/task_detail.html'

class TaskCreateView(CreateView):
    model = Task
    template_name = 'task/task_create.html'
    form_class = TaskCreateForm
    success_url = reverse_lazy('task:task-list')

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'task/task_edit.html'
    form_class = TaskCreateForm
    update_status = False

    def get_success_url(self):
        return reverse_lazy('task:task-list')

    def form_valid(self, form):
        if form.instance.completed_flag == True:
            self.object.completed_date = date.today()
            return super(TaskUpdateView, self).form_valid(form)
        else:
            return super(TaskUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if self.update_status == True:
            self.object = self.get_object()
            if self.object.completed_flag == False:
                self.object.completed_date = date.today()
                self.object.completed_flag = True
            else:
                self.object.completed_date = None
                self.object.completed_flag = False
            self.object.save()
            return redirect('task:task-list')
        else:
            return super().post(self, request, *args, **kwargs)



class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('task:task-list')

