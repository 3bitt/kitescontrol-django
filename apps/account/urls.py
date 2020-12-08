from django.contrib import admin
from django.urls import path
from .views import (MainLoginView)

app_name = 'account'
urlpatterns = [
    path('', MainLoginView.as_view(), name='login'),
]
