from django.contrib.auth.views import LoginView, redirect_to_login
from django.contrib.auth.mixins import PermissionRequiredMixin


class MainLoginView(LoginView):
    template_name = 'account/login.html'
    success_url = '/'
