from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    InstructorHomeView,
    )

app_name = 'instructor'
urlpatterns = [
path('', login_required(InstructorHomeView.as_view()), name='instructor-home'),
    # path('create/', StudentCreateView.as_view(), name='student-create'),
    # path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    # path('<int:pk>/edit/', StudentUpdateView.as_view(editMode=True), name='student-detail-edit' ),
    # path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student-delete'),
    # path('q', StudentSearchView.as_view(), name='student-search'),


]
