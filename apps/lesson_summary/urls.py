from datetime import datetime
from .views import LessonSummaryView
from django.urls import path
from django.urls.converters import register_converter
from django.contrib.auth.decorators import login_required
from lesson.urls import DateConverter


# register_converter(DateConverter, 'date')

app_name = 'lesson_summary'
urlpatterns = [
    path('', login_required(LessonSummaryView.as_view()), name='lesson-summary'),
    path('<date:summary_date>/', login_required(LessonSummaryView.as_view()), name='lesson-summary'),

]