from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('id', 'value', 'user', 'source')

class ExpensePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('value', 'source')