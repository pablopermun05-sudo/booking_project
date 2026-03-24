from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    return render(request, "bookings/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bookings/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "bookings/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name","last_name","username", "email", "phone_number")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bookings/register.html", {
                "message": "Las contraseñas deben coincidir.",
                "form": form
            })

    else:
        return render(request, "bookings/register.html", {
            "form": RegisterForm()
        })
