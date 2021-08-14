from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import (
    SearchHomeView,
    SearchRentalAjaxView,
    SearchStudentAjaxView,
    SearchLessonAjaxView,
)

app_name = 'search'
urlpatterns = [
    path('', login_required(SearchHomeView.as_view()), name='search-home'),
    path(
        'student/', login_required(SearchStudentAjaxView.as_view()), name='search-student'
    ),
    path('lesson/', login_required(SearchLessonAjaxView.as_view()), name='search-lesson'),
    path('rental/', login_required(SearchRentalAjaxView.as_view()), name='search-rental'),
]
