from django.urls import path
from .views import LessonListView, LessonCreateView, LessonDeleteView
from django.contrib.auth.decorators import login_required


app_name = 'lesson'
urlpatterns = [
    path('', login_required(LessonListView.as_view()), name='lesson-list'),
    path('create/', login_required(LessonCreateView.as_view()), name='lesson-create'),
    # path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    # path('<int:pk>/edit/', StudentUpdateView.as_view(editMode=True), name='student-detail-edit' ),
    path('delete/<int:pk>/', login_required(LessonDeleteView.as_view()), name='lesson-delete'),
    # path('q', StudentSearchView.as_view(), name='student-search'),


]