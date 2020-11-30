from django.contrib import admin
from django.urls import path
from .views import StudentCreateView, StudentListView, StudentDetailView, StudentDeleteView

app_name = 'student'
urlpatterns = [
    path('', StudentListView.as_view(), name='student-list'),
    path('create/', StudentCreateView.as_view(), name='student-create'),
    path('<int:id>/', StudentDetailView.as_view(), name='student-detail'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student-delete'),
    
]
