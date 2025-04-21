import django_filters
from .models import *

class ExpenseFilter(django_filters.FilterSet):
    class Meta:
        model = Expense
        fields = {'value': ['exact', 'lt', 'gt', 'range'],
                  'source': ['exact'],
                  'user': ['exact'],
                  'id': ['exact']}