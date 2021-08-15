from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, reverse, reverse_lazy
from .views import (
    AccountChangeActiveStatus,
    AccountCreateUserView,
    AccountDeleteUserView,
    AccountDetailUserView,
    AccountUpdateUserView,
    MainLoginView,
)
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('', MainLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'create-user/',
        login_required(AccountCreateUserView.as_view()),
        name='create-user',
    ),
    path(
        'user/<int:pk>/',
        login_required(AccountDetailUserView.as_view()),
        name='detail-user',
    ),
    path(
        'user/update/<int:pk>/',
        login_required(AccountUpdateUserView.as_view()),
        name='update-user',
    ),
    path(
        'user/delete/<int:pk>/',
        login_required(AccountDeleteUserView.as_view()),
        name='delete-user',
    ),
    path(
        'user/deactivate/<int:pk>/',
        login_required(AccountChangeActiveStatus.as_view()),
        name='deactivate-user',
    ),
    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('account:password_reset_done')
        ),
        name='reset_password',
    ),
    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('account:password_reset_complete')
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
]
