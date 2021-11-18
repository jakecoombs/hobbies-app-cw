import os

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from . import database
from .models import PageView, User
from .forms import LoginForm, SignupForm


@login_required
def index(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index
    view. """
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'hobbies/bootstrap.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })


def health(request):
    """Takes an request as a parameter and gives the count of pageview objects as reponse"""
    return HttpResponse(PageView.objects.count())


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
            authenticated_user = auth.authenticate(username=username, password=password)
            if authenticated_user is not None:
                auth.login(request, authenticated_user)
                return redirect("hobbies:home")

    # GET request (or could not authenticate)
    return render(request, 'hobbies/signup.html', { 'form': SignupForm })


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
                return redirect("hobbies:home")

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
    return redirect("hobbies:home")
