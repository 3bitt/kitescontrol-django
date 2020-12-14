from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView


app_name = 'task'
urlpatterns = [
    path('', login_required(TaskListView.as_view()), name='task-list'),
    path('create', login_required(TaskCreateView.as_view()), name='task-create'),
    path('<int:pk>/edit/', login_required(TaskUpdateView.as_view()), name='task-edit' ),
    path('<int:pk>/updateStatus/', login_required(TaskUpdateView.as_view(update_status=True)), name='task-update-status'),
    # path('q', StudentSearchView.as_view(), name='student-search'),


]
