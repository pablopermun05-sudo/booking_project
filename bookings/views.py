from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from .models import User, Property
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
class SearchForm(forms.Form):
    DESTINATION = [
        ('', '¿A dónde vas?'),
        ('Palos de la Frontera', 'Palos de la Frontera'),
        ('Mazagón', 'Mazagón')
    ]
    NUM_CHOICES = [(i, str(i)) for i in range(1, 11)]
    CHOICES_WITH_ZERO = [(i, str(i)) for i in range(0, 11)]

    location = forms.ChoiceField(label="Lugar", choices=DESTINATION)
    initial_date = forms.DateField(
        label="Entrada",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    final_date = forms.DateField(
        label="Salida",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    adults = forms.ChoiceField(label="Adultos", choices=NUM_CHOICES, required=False, initial=1)
    children = forms.ChoiceField(label="Niños", choices=CHOICES_WITH_ZERO, required=False, initial=0)
    rooms = forms.ChoiceField(label="Habitaciones", choices=NUM_CHOICES, required=False, initial=1)
    pets = forms.BooleanField(required=False, label="Mascotas")

def index(request):

    return render(request, "bookings/index.html", {
        "form": SearchForm()
    })

class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Usuario o contraseña incorrectos. Inténtalo de nuevo.",
    }

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
        
        return render(request, "bookings/login.html", {
            "form": form
        })
    else:
        return render(request, "bookings/login.html", {
            "form": LoginForm()
        })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name","last_name","username", "email", "phone_number")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Elimina los textos de ayuda
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bookings/register.html", {
                "form": form
            })
    else:
        return render(request, "bookings/register.html", {
            "form": RegisterForm()
        })
