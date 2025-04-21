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
import datetime
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ExpenseFilter

class ExpenseView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter
    def get(self, request):
        expenses = Expense.objects.all().filter(active=True)

        for backend in list(self.filter_backends):
            expenses = backend().filter_queryset(request, expenses, self)

        paginator = PageNumberPagination()
        paged = paginator.paginate_queryset(expenses, request)

        return paginator.get_paginated_response(ExpenseSerializer(paged, many=True).data)

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

class ExpenseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if id is None:
            return Response({'error': 'Id is required'}, status=status.HTTP_400_BAD_REQUEST)

        expense = Expense.objects.filter(active=True).filter(id=id).first()
        if expense is None:
            return Response({'error': 'Expense does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return Response(ExpenseSerializer(expense).data, status=status.HTTP_200_OK)

    def put(self, request, id):
        source = request.data.get('source')
        value = request.data.get('value')

        if id is None:
            return Response({'error': 'Id is required'}, status=status.HTTP_400_BAD_REQUEST)

        expense = Expense.objects.filter(active=True).filter(id=id).first()
        if expense is None:
            return Response({'error': 'Expense does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if source is not None:
            expense.source = source

        if value is not None:
            expense.value = value

        expense.save()

        return Response(ExpenseSerializer(expense).data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        if id is None:
            return Response({'error': 'Id is required'}, status=status.HTTP_400_BAD_REQUEST)

        expense = Expense.objects.filter(active=True).filter(id=id).first()
        if expense is None:
            return Response({'error': 'Expense does not exist'}, status=status.HTTP_404_NOT_FOUND)

        expense.active = False
        expense.updated_at = str(datetime.datetime.now())
        expense.save()

        return Response(ExpenseSerializer(expense).data, status=status.HTTP_200_OK)

class UserView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]
    def get(self, request):
        if request.user.is_superuser:
            users = User.objects.all().filter(is_active=True)

            paginator = PageNumberPagination()
            paged = paginator.paginate_queryset(users, request)

            serializer = UserSerializer(paged, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response("{'error':'User does not have access'}", status=403)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(is_active=True).filter(email=email).exists():
            return Response({'error': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=email, email=email, password=password)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        if request.user.is_superuser:
            if id is None:
                return Response({'error': 'Id is required'}, status=status.HTTP_400_BAD_REQUEST)

            if not request.user.is_superuser:
                return Response({'error': 'Logged user is not superuser'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(is_active=True).filter(id=id).first()
            if user is None:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

            user.is_active = False
            user.updated_at = str(datetime.datetime.now())
            user.save()

            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response("{'error':'User does not have access'}", status=403)


    def put(self, request, id):
        if request.user.is_superuser:
            username = request.data.get('username')

            if username is None:
                return Response({'error': 'Username required'}, status=status.HTTP_400_BAD_REQUEST)

            if id is None:
                return Response({'error': 'Id is required'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(is_active=True).filter(id=id).first()
            if user is None:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

            user.username = username
            user.save()

            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response("{'error':'User does not have access'}", status=403)

    def get(self, request, id):
        if request.user.is_superuser:
            if id is None:
                return Response({'error': 'Id is required'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(is_active=True).filter(id=id).first()
            if user is None:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response("{'error':'User does not have access'}", status=403)


class UserLogin(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"user": UserSerializer(request.user).data}, status=status.HTTP_200_OK)

class JWTView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):

        saved = User.objects.filter(is_active=True).filter(email=request.data.get('email')).first()
        if not saved:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if not saved.check_password(raw_password=request.data.get('password')):
            return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(saved)

        return Response({
            'refresh': str(refresh),
            'token': str(refresh.access_token)
        }, status=status.HTTP_200_OK)