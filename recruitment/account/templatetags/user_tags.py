from django import template
from django.contrib.auth.models import AnonymousUser

register = template.Library()


@register.simple_tag
def user_token(user):
    if issubclass(user.__class__, AnonymousUser):
        return "Anonymous"
    return user.generate_token()
