from django.urls import path
from .views import HomeView

app_name = 'dashboard'
urlpatterns = [
    path('', HomeView.as_view(), name='dashboard-home')
]
