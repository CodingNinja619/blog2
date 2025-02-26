from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from .forms import LoginForm, RegisterForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from blog.models import User


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])

            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Login successfully")
                else:
                    return HttpResponse("Account is disabled")
            else:
                raise PermissionDenied("Invalid username or password")
        
    else:
        form = LoginForm()
        
        return render(request, "registration/login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("blog:post_list")

def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            user = form.save(commit=False)
            user.set_password(cd["password1"])
            user.save()
        
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})