from django.urls import path
from .views import SearchHomeView, SearchStudentAjaxView

app_name = 'search'
urlpatterns = [
    path('', SearchHomeView.as_view(), name='search-home'),
    path('student/', SearchStudentAjaxView.as_view(), name='search-student'),
]
