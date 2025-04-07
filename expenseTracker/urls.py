from django.contrib import admin
from django.urls import path
from expenseTracker.views import *

urlpatterns = [
    path('expenses', ExpenseAPIView.as_view(), name='expenses'),
    path('users', UserAPIView.as_view(), name='users'),
    path('', UserLogin.as_view(), name='home'),
    path('login', JWTView.as_view(), name='login')
]
