from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Expense
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password

class ExpenseAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        expenses = Expense.objects.all()
        return Response(ExpenseSerializer(expenses, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExpensePostSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('value') is None:
            return Response({'error': 'Value is null'}, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('source') is None:
            return Response({'error': 'Source is null'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
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

class UserLogin(APIView):
    def post(self, request):
        saved = User.objects.filter(username=request.data.get('email')).first()
        if not saved:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if not saved.check_password(raw_password=request.data.get('password')):
            return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

        #user = authenticate(request, username= request.data.get('email'), password=request.data.get('password'))

        """if user is not None:
            login(request=request, user=user)
            return Response({"email": request.data.get('email')}, status=status.HTTP_200_OK)"""

    def get(self, request):
        return Response({"user": UserSerializer(request.user).data}, status=status.HTTP_200_OK)

class JWTView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):

        saved = User.objects.filter(username=request.data.get('email')).first()
        if not saved:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if not saved.check_password(raw_password=request.data.get('password')):
            return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(saved)

        return Response({
            'refresh': str(refresh),
            'token': str(refresh.access_token)
        }, status=status.HTTP_200_OK)