from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import User


def signup_view(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if User.objects.filter(username=username).exists():

            return render(request, "login.html", {
                "signup_error": "Username is already taken.",
                "signup_username": username,
                "signup_email": email,
                "show_signup": True,
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect("home")

    return redirect("login")


def logout_view(request):
    logout(request)
    return redirect("login")


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        else:

            return render(
                request,
                "login.html",
                {
                    "error": "Invalid username or password."
                }
            )

    return render(request, "login.html")