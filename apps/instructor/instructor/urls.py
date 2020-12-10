from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    InstructorHomeView,
    InstructorListView,
    InstructorCreateView,
    InstructorUpdateView,
    InstructorDetailView,
    InstructorDeleteView
    )

app_name = 'instructor'
urlpatterns = [
    path('', login_required(InstructorHomeView.as_view()), name='instructor-home'),
    path('list', login_required(InstructorListView.as_view()), name='instructor-list'),
    path('create/', InstructorCreateView.as_view(), name='instructor-create'),
    path('<int:pk>/', InstructorDetailView.as_view(), name='instructor-detail'),
    path('<int:pk>/edit/', InstructorUpdateView.as_view(editMode=True), name='instructor-detail-edit' ),
    path('delete/<int:pk>/', InstructorDeleteView.as_view(), name='instructor-delete'),
    # path('q', StudentSearchView.as_view(), name='student-search'),


]
