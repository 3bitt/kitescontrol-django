from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import HomeView

app_name = 'dashboard'
urlpatterns = [
    path('', login_required(HomeView.as_view()), name='dashboard-home')
]
