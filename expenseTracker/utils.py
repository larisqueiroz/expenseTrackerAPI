from django.db import models

class Category(models.IntegerChoices):
    GROCERIES = 1,
    LEISURE = 2
    ELECTRONICS = 3
    UTILITIES = 4
    CLOTHING = 5
    HEALTH = 6
    EDUCATION = 7
    FITNESS = 8
    OTHER = 9