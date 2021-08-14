from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views import PayrollByDate, PayrollHomeView


app_name = 'payroll'
urlpatterns = [
    path('', login_required(PayrollHomeView.as_view()), name='payroll-home'),
    path(
        'calculatepayroll/',
        login_required(PayrollByDate.as_view()),
        name='payroll-by-date',
    ),
]
