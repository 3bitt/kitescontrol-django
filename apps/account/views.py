from django.contrib.auth.views import LoginView, redirect_to_login
from django.contrib.auth.mixins import PermissionRequiredMixin


class UserAccessMixin(PermissionRequiredMixin):

    login_url = 'account:login'

    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(),
                                    self.get_login_url(), self.get_redirect_field_name())

        # if not self.has_permission():
        #     return redirect('/')

        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)



class MainLoginView(LoginView):
    template_name = 'account/login.html'
    success_url = '/'
