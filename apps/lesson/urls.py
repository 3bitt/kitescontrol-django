from django.urls import path
from .views import LessonCompleteView, LessonConfirmView, LessonListView, LessonCreateView, LessonDeleteView, LessonStartView, LessonUpdateView
from django.contrib.auth.decorators import login_required


app_name = 'lesson'
urlpatterns = [
    path('', login_required(LessonListView.as_view()), name='lesson-list'),
    path('create/', login_required(LessonCreateView.as_view()), name='lesson-create'),
    # path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('<int:pk>/edit/', LessonUpdateView.as_view(), name='lesson-edit' ),
    path('<int:pk>/setInProgress/', LessonStartView.as_view(), name='lesson-set-in-progress' ),
    path('<int:pk>/confirm/', LessonConfirmView.as_view(), name='lesson-confirm' ),
    path('<int:pk>/complete/', LessonCompleteView.as_view(), name='lesson-complete', ),
    path('delete/<int:pk>/', login_required(LessonDeleteView.as_view()), name='lesson-delete'),
    # path('q', StudentSearchView.as_view(), name='student-search'),


]