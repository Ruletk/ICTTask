import logging

from account.forms import PasswordChangeForm
from account.forms import UserEducationForm
from account.forms import UserLoginForm
from account.forms import UserRegisterForm
from account.forms import UserSecurityForm
from account.forms import UserSettingsForm
from account.models import Education
from account.models import User
from account.services.profile import change_education
from account.services.profile import change_password
from account.services.profile import change_security
from account.services.profile import change_settings
from django.contrib import messages
from django.contrib.auth import login as base_login
from django.contrib.auth import logout as base_logout
from django.shortcuts import redirect
from django.shortcuts import render
from jobs.forms import CreateResumeForm
from miscs.decorators import anonymous_required
from miscs.decorators import login_required
from miscs.model_features import get_or_none

# Create your views here.
logger = logging.getLogger(__name__)


@anonymous_required
def login(request):
    if request.method == "GET":
        form = UserLoginForm()
        return render(request, "account/login.html", {"form": form})
    form = UserLoginForm(request.POST)
    if form.is_valid():
        user = get_or_none(User, email=form.cleaned_data.get("email"))
        if not user.check_password(form.cleaned_data.get("password")):
            user = None
        if user is not None:
            base_login(request, user)
            if not form.cleaned_data.get("remember"):
                request.session.set_expiry(0)
            messages.success(request, "You have successfully logged in.")
            return redirect("jobs:index")
        form.add_error("__all__", "Invalid email or password")
    else:
        messages.error(request, "Something went wrong.")
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
        return redirect("account:profile_settings")
    return render(request, "account/register.html", {"form": form})


def profile_detail(request, user_id):
    user = User.objects.get(id=user_id)
    context = {"user": user}
    return render(request, "account/profile_detail.html", context)


@login_required
def profile(request):
    context = {"user": request.user}
    return render(request, "account/profile_detail.html", context)


@login_required
def profile_settings(request):
    form = UserSettingsForm()
    if request.method == "GET":
        context = {"user": request.user, "form": form}
        return render(request, "account/profile_settings.html", context)
    form = UserSettingsForm(request.POST)
    if form.is_valid():
        change_settings(request.user, form, request.FILES)
        messages.success(request, "You have successfully changed your settings.")
        return redirect("account:profile")
    else:
        messages.error(request, "Something went wrong.")
        context = {"user": request.user, "form": form}
        return render(request, "account/profile_settings.html", context)


@login_required
def profile_education(request):
    if request.method == "GET":
        context = {
            "user": request.user,
            "form": UserEducationForm(),
            "degrees": Education.DEGREES,
        }
        return render(request, "account/profile_education.html", context)
    form = UserEducationForm(request.POST)
    if form.is_valid():
        change_education(request.user, form)
        messages.success(request, "You have successfully changed your education.")
        return redirect("account:profile")
    else:
        messages.error(request, "Something went wrong.")
        context = {"user": request.user, "form": form, "degrees": Education.DEGREES}
        return render(request, "account/profile_education.html", context)


@login_required
def profile_security(request):
    if request.method == "GET":
        context = {
            "user": request.user,
            "form": UserSecurityForm(),
            "password": PasswordChangeForm(),
        }
        return render(request, "account/profile_security.html", context)

    password_form = PasswordChangeForm(request.POST)
    form = UserSecurityForm(request.POST)

    if password_form.is_valid():
        user = change_password(request.user, password_form)
        base_login(request, user)
        messages.success(request, "You have successfully changed your password.")
        return redirect("account:profile")

    if form.is_valid():
        change_security(request.user, form)
        messages.success(
            request, "You have successfully changed your security settings."
        )
        return redirect("account:profile")
    messages.error(request, "Something went wrong.")
    context = {"user": request.user, "form": form, "password_form": password_form}
    return render(request, "account/profile_security.html", context)


@login_required
def profile_resume(request):
    if request.method == "GET":
        form = CreateResumeForm()
        context = {"user": request.user, "form": form}
        return render(request, "account/profile_resume.html", context)

    form = CreateResumeForm(request.POST)
    if form.is_valid():
        form.instance = request.user
        form.save()
        messages.success(request, "You have successfully created your resume.")
        return redirect("account:profile")
    messages.error(request, "Error while creating resume.")
    print(form.errors)
    context = {"user": request.user, "form": form}
    return render(request, "account/profile_resume.html", context)
