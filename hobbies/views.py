import os

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import User
from .forms import LoginForm, SignupForm


@login_required
def index(request):
    """Render the home page of the app"""

    return render(request, 'hobbies/index.html', {
        'title': 'Hobbies',
    })


@login_required
def users(request):
    """Render the home page of the app"""

    return render(request, 'hobbies/users.html', {
        'title': 'Hobbies: Users',
    })


def health(request):
    """Responds with code 200 to show that the app is up and running"""
    return HttpResponse(200)


def signup(request):
    form = SignupForm()

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            password_confirmation = form.cleaned_data["password_confirmation"]
            email = form.cleaned_data["email"]
            dob = form.cleaned_data["dob"]

            # validation
            error_message = None
            if User.objects.all().filter(username=username).exists():
                error_message = "User already exists."

            if not error_message and password != password_confirmation:
                error_message = "Passwords do not match."

            if error_message:
                # could not authenticate
                return render(request, "hobbies/error.html", {
                    "error": error_message
                })

            # create new user
            new_user = User.objects.create(username=username,
                                           email=email,
                                           dob=dob)

            # set password
            new_user.set_password(password)
            new_user.save()

            # create session
            authenticated_user = auth.authenticate(
                username=username, password=password)
            if authenticated_user is not None:
                auth.login(request, authenticated_user)
                return redirect("home")

    # GET request (or could not authenticate)
    return render(request, 'hobbies/signup.html', {'form': SignupForm})


def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # create session
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("home")

            # could not authenticate
            return render(request, "hobbies/error.html", {
                "error": "User is not registered. Please create an account."
            })

        # invalid form
        return render(request, "hobbies/login.html", {
            "form": form
        })

    return render(request, "hobbies/login.html", {"form": form})


@login_required
def logout(request):
    auth.logout(request)
    return redirect("home")
