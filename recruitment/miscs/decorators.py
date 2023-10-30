from functools import wraps

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
