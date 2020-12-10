from django.contrib import admin
from django.urls import path
from .views import (MainLoginView)
from django.contrib.auth.views import LogoutView

app_name = 'account'
urlpatterns = [
    path('', MainLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
