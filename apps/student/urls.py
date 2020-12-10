from django.contrib import admin
from django.urls import path
from .views import (
    StudentCreateView,
    StudentListView,
    StudentDetailView,
    StudentDeleteView,
    StudentSearchView,
    StudentUpdateView, )

app_name = 'student'
urlpatterns = [
    path('', StudentListView.as_view(), name='student-list'),
    path('create/', StudentCreateView.as_view(), name='student-create'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('<int:pk>/edit/', StudentUpdateView.as_view(editMode=True), name='student-detail-edit' ),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student-delete'),
    path('q', StudentSearchView.as_view(), name='student-search'),

    
]
