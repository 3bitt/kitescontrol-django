from datetime import datetime
from django.urls.conf import re_path
from .views import LessonSummaryView, ShowDifferentSummaryRedirectView
from django.urls import path
from django.urls.converters import register_converter
from django.contrib.auth.decorators import login_required
from lesson.urls import DateConverter


# register_converter(DateConverter, 'date')

app_name = 'lesson_summary'
urlpatterns = [
    path('', login_required(LessonSummaryView.as_view()), name='lesson-summary'),
    path('<date:summary_date>/', login_required(LessonSummaryView.as_view()), name='lesson-summary'),
    path('search', login_required(ShowDifferentSummaryRedirectView.as_view()), name='lesson-summary-show'),
    # re_path(r'^search/(?P<summary_date>\d{4}-\d{2}-\d{2})/$', login_required(LessonSummaryView.as_view()), name='lesson-summary'),

]