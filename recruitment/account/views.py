import logging

from account.forms import PasswordChangeForm
from account.forms import UserEducationForm
from account.forms import UserLoginForm
from account.forms import UserRegisterForm
from account.forms import UserSecurityForm
from account.forms import UserSettingsForm
from account.models import Education
from account.models import User
from django.contrib import messages
from django.contrib.auth import login as base_login
from django.contrib.auth import logout as base_logout
from django.shortcuts import redirect
from django.shortcuts import render
from miscs.decorators import anonymous_required
from miscs.decorators import login_required

# Create your views here.
logger = logging.getLogger(__name__)


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


def profile_detail(request, id):
    user = User.objects.get(id=id)
    context = {"user": user}
    return render(request, "account/profile_detail.html", context)


def profile(request):
    context = {"user": request.user}
    return render(request, "account/profile_detail.html", context)


def profile_settings(request):
    form = UserSettingsForm()
    if request.method == "GET":
        context = {"user": request.user, "form": form}
        return render(request, "account/profile_settings.html", context)
    form = UserSettingsForm(request.POST)
    form.instance = request.user
    if form.is_valid():
        if request.FILES.get("avatar"):
            request.user.avatar.delete()
            request.user.avatar = request.FILES.get("avatar")
        form.save()
        messages.success(request, "You have successfully changed your settings.")
        return redirect("account:profile")
    else:
        messages.error(request, "Something went wrong.")
        context = {"user": request.user, "form": form}
        return render(request, "account/profile_settings.html", context)


def profile_education(request):
    if request.method == "GET":
        context = {
            "user": request.user,
            "form": UserEducationForm(),
            "degrees": Education.DEGREES,
        }
        return render(request, "account/profile_education.html", context)
    form = UserEducationForm(request.POST)
    form.instance = request.user
    if form.is_valid():
        form.save()
        messages.success(request, "You have successfully changed your education.")
        return redirect("account:profile")
    else:
        messages.error(request, "Something went wrong.")
        context = {"user": request.user, "form": form, "degrees": Education.DEGREES}
        return render(request, "account/profile_education.html", context)


def profile_security(request):
    if request.method == "GET":
        context = {
            "user": request.user,
            "form": UserSecurityForm(),
            "password": PasswordChangeForm(),
        }
        return render(request, "account/profile_security.html", context)
    redirected = False
    password_form = PasswordChangeForm(request.POST)
    form = UserSecurityForm(request.POST)
    if password_form.is_valid():
        password_form.instance = request.user
        user = password_form.save()
        base_login(request, user)
        messages.success(request, "You have successfully changed your password.")
        redirected = True
    else:
        messages.error(request, "Something went wrong.")
        context = {"user": request.user, "form": form, "password_form": password_form}
        return render(request, "account/profile_security.html", context)

    if form.is_valid():
        form.instance = request.user
        form.save()
        messages.success(
            request, "You have successfully changed your security settings."
        )
        redirected = True

    if redirected:
        return redirect("account:profile")
    return render(request, "account/profile_security.html")


def profile_resume(request):
    return render(request, "account/profile_resume.html")
