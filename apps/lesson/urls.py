from datetime import datetime
from django.conf.urls import include, url
from django.urls import path, re_path
from django.urls.converters import register_converter
from .views import LessonCompleteView, LessonConfirmView, LessonListView, LessonCreateView, LessonDeleteView, LessonStartView, LessonUpdateView
from django.contrib.auth.decorators import login_required


class DateConverter:
    regex = '\d{2}-\d{2}-\d{4}'

    def to_python(self, value):
        return datetime.strptime(value, '%d-%m-%Y')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'date')

app_name = 'lesson'
urlpatterns = [
    path('schedule/', login_required(LessonListView.as_view()), name='lesson-list'),
    path('schedule/<date:schedule_date>/', login_required(LessonListView.as_view()), name='lesson-list'),
    path('create/', login_required(LessonCreateView.as_view()), name='lesson-create'),
    path('<int:pk>/edit/', login_required(LessonUpdateView.as_view()), name='lesson-edit' ),
    path('<int:pk>/setInProgress/', login_required(LessonStartView.as_view()), name='lesson-set-in-progress' ),
    path('<int:pk>/confirm/', login_required(LessonConfirmView.as_view()), name='lesson-confirm' ),
    path('<int:pk>/complete/', login_required(LessonCompleteView.as_view()), name='lesson-complete', ),
    path('delete/<int:pk>/', login_required(LessonDeleteView.as_view()), name='lesson-delete'),

    path('summary/', include('lesson_summary.urls'))
]