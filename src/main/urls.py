from django.contrib import admin
from django.urls import path
from .views import Index

app_name = 'main'
urlpatterns = [
    path('', Index.as_view()),
]