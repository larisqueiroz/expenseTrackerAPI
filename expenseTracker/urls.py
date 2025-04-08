from django.contrib import admin
from django.urls import path
from expenseTracker.views import *

urlpatterns = [
    path('expenses', ExpenseView.as_view(), name='expenses'),
    path('expenses/<uuid:id>', ExpenseDetailView.as_view(), name='expensesdetail'),
    path('users', UserView.as_view(), name='users'),
    path('users/<int:id>', UserDetailView.as_view(), name='usersdetail'),
    path('', UserLogin.as_view(), name='home'),
    path('login', JWTView.as_view(), name='login')
]
