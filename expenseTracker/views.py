from django.shortcuts import render
from rest_framework.views import APIView
from .models import Expense
from .serializers import ExpenseSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class ExpenseAPIView(APIView):
    def get(self, request):
        expenses = Expense.objects.all()
        return Response(ExpenseSerializer(expenses, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.data.get('user') is None:
            return Response({'error': 'User is null'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=email).exists():
            return Response({'error': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=email, email=email, password=password)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
