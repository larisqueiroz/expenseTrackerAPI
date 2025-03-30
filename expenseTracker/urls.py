from django.contrib import admin
from django.urls import path
from expenseTracker.views import *

urlpatterns = [
    path('expenses', ExpenseAPIView.as_view(), name='expenses'),
    path('users', UserAPIView.as_view(), name='users')
]
