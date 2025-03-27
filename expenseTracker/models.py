import uuid

from django.db import models
from django.contrib.auth.models import User
from .utils import Category

class Base(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4())
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Expense(Base):
    value = models.FloatField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    source = models.IntegerField(choices=Category.choices, null=True)

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'