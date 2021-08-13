from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import (
    StudentCreateView,
    StudentListView,
    StudentDetailView,
    StudentDeleteView,
    StudentSearchView,
    StudentUpdateView,
)

app_name = 'student'
urlpatterns = [
    path('', login_required(StudentListView.as_view()), name='student-list'),
    path('create/', login_required(StudentCreateView.as_view()), name='student-create'),
    path('<int:pk>/', login_required(StudentDetailView.as_view()), name='student-detail'),
    path(
        '<int:pk>/edit/',
        login_required(StudentUpdateView.as_view(editMode=True)),
        name='student-detail-edit',
    ),
    path(
        'delete/<int:pk>/',
        login_required(StudentDeleteView.as_view()),
        name='student-delete',
    ),
    path('q', login_required(StudentSearchView.as_view()), name='student-search'),
]
