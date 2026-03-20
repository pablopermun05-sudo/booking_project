from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username

class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='properties/')
    price_per_night = models.DecimalField(max_digits=7, decimal_places=2)
    children = models.PositiveIntegerField()
    adults = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    allow_pets = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="properties")
    
    class Meta:
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedades"

    def __str__(self):
        return self.title

class Booking(models.Model):
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="bookings")
    initial_date = models.DateField()
    final_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        return f"Reserva de {self.tenant} en {self.property.title}"