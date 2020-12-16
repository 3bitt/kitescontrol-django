from django.contrib import admin
from django.urls import path, reverse, reverse_lazy
from .views import (MainLoginView)
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('', MainLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('reset_password/',
            auth_views.PasswordResetView.as_view(
                success_url = reverse_lazy('account:password_reset_done')),
        name='reset_password'),

    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            success_url = reverse_lazy('account:password_reset_complete')),
        name='password_reset_confirm'),

    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),

]
