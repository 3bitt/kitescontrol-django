from datetime import datetime
from django.conf.urls import include, url
from django.urls import path, re_path
from django.urls.converters import register_converter
from .views import RentalCreateView
from django.contrib.auth.decorators import login_required


app_name = 'rental'
urlpatterns = [
    path('create/', login_required(RentalCreateView.as_view()), name='rental-create'),

]