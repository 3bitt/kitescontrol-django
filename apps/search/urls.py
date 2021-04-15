from django.urls import path
from .views import SearchHomeView

app_name = 'search'
urlpatterns = [
    path('', SearchHomeView.as_view(), name='search-home')
]
