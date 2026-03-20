from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class User(AbstractUser):
    pass

class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=64)
    image = models.ImageField()
    price_per_night = models.DecimalField(max_digits=7, decimal_places=2)
    children = models.PositiveIntegerField()
    adults = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    allow_pets = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="properties")