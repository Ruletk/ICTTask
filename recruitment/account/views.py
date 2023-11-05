from account.forms import UserLoginForm
from account.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login as base_login
from django.contrib.auth import logout as base_logout
from django.shortcuts import redirect
from django.shortcuts import render
from miscs.decorators import anonymous_required
from miscs.decorators import login_required

# Create your views here.


@anonymous_required
def login(request):
    if request.method == "GET":
        form = UserLoginForm()
        return render(request, "account/login.html", {"form": form})
    form = UserLoginForm(request.POST)
    if form.is_valid():
        base_login(request, form.cleaned_data)
        messages.success(request, "You have successfully logged in.")
        return redirect("jobs:index")
    else:
        return render(request, "account/login.html", {"form": form})


@login_required
def logout(request):
    base_logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("jobs:index")


@anonymous_required
def register(request):
    if request.method == "GET":
        form = UserRegisterForm()
        return render(request, "account/register.html", {"form": form})
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        base_login(request, user)
        return redirect("jobs:index")
    return render(request, "account/register.html", {"form": form})


def profile_detail(request, username):
    return render(request, "account/profile_detail.html")
