from django.urls import path, include
from .views import PayrollByDate, PayrollHomeView


app_name = 'payroll'
urlpatterns = [
    path('', PayrollHomeView.as_view(), name='payroll-home'),
    path('calculatepayroll/', PayrollByDate.as_view(), name='payroll-by-date'),

]
