from datetime import datetime
from django.conf.urls import include, url
from django.urls import path, re_path
from django.urls.converters import register_converter
from .views import RentalCreateView, RentalDeleteView, RentalDetailView, RentalUpdateView
from django.contrib.auth.decorators import login_required


app_name = 'rental'
urlpatterns = [
    path('create/', login_required(RentalCreateView.as_view()), name='rental-create'),
    path('detail/<int:pk>', login_required(RentalDetailView.as_view()), name='rental-detail'),
    path('detail/<int:pk>/edit', login_required(RentalUpdateView.as_view()), name='rental-edit'),
    path('detail/<int:pk>/delete', login_required(RentalDeleteView.as_view()), name='rental-delete'),

]