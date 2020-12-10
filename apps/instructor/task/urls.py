from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import TaskListView, TaskCreateView


app_name = 'task'
urlpatterns = [
    path('', login_required(TaskListView.as_view()), name='task-list'),
    path('create', login_required(TaskCreateView.as_view()), name='task-create'),
    # path('list', login_required(InstructorListView.as_view()), name='instructor-list'),
    # path('create/', login_required(InstructorCreateView.as_view()), name='instructor-create'),
    # path('<int:pk>/', login_required(InstructorDetailView.as_view()), name='instructor-detail'),
    # path('<int:pk>/edit/', login_required(InstructorUpdateView.as_view(editMode=True)), name='instructor-detail-edit' ),
    # path('delete/<int:pk>/', login_required(InstructorDeleteView.as_view()), name='instructor-delete'),
    # path('q', StudentSearchView.as_view(), name='student-search'),


]
