import json
from functools import wraps

from account.models import Token
from django.http import JsonResponse
from django.shortcuts import redirect


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account:login")
        return func(request, *args, **kwargs)

    return wrapper


def anonymous_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("jobs:index")
        return func(request, *args, **kwargs)

    return wrapper


def post_only(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.method != "POST":
            return JsonResponse({"status": "error", "message": "post only"})
        return func(request, *args, **kwargs)

    return wrapper


def check_token(func):
    """Checking token from json data
    Automatically serializing json data to request.json_data
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        json_data = json.loads(request.body)
        user = Token.find_user(json_data.get("token"))
        if user is None:
            return JsonResponse({"status": "error", "message": "token not found"})
        request.user = user
        request.json_data = json_data
        return func(request, *args, **kwargs)

    return wrapper


def employer_only(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and request.user.is_employer
            or request.user.is_anonymous
        ):
            return func(request, *args, **kwargs)
        return redirect("jobs:index")

    return wrapper


def worker_only(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and request.user.is_employer is False
            or request.user.is_anonymous
        ):
            return func(request, *args, **kwargs)
        return redirect("jobs:employer")

    return wrapper
