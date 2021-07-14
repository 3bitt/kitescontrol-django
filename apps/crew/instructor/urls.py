from django.urls import path
from django.contrib.auth.decorators import login_required
from django.urls.conf import include
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
    path('list/', login_required(InstructorListView.as_view()), name='instructor-list'),
    path('create/', login_required(InstructorCreateView.as_view()), name='instructor-create'),
    path('<int:pk>/', login_required(InstructorDetailView.as_view()), name='instructor-detail'),
    path('<int:pk>/edit/', login_required(InstructorUpdateView.as_view(editMode=True)), name='instructor-detail-edit'),
    path('delete/<int:pk>/', login_required(InstructorDeleteView.as_view()), name='instructor-delete'),

    path('task/', include('crew.task.urls')),
    path('payroll/', include('crew.payroll.urls')),

]
