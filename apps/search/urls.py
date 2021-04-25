from django.urls import path
from .views import SearchHomeView, SearchRentalAjaxView, SearchStudentAjaxView, SearchLessonAjaxView

app_name = 'search'
urlpatterns = [
    path('', SearchHomeView.as_view(), name='search-home'),
    path('student/', SearchStudentAjaxView.as_view(), name='search-student'),
    path('lesson/', SearchLessonAjaxView.as_view(), name='search-lesson'),
    path('rental/', SearchRentalAjaxView.as_view(), name='search-rental'),
]
