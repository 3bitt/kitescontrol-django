from django.contrib import admin
from django.urls import path
from .views import ListStudentView, CreateStudentView

app_name = 'student'
urlpatterns = [
    path('', ListStudentView.as_view(), name='student-list'),
    path('create/', CreateStudentView.as_view(), name='student-create')
    
]
