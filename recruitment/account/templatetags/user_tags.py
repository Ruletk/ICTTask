from django import template
from django.contrib.auth.models import AnonymousUser

register = template.Library()


@register.simple_tag
def user_token(user):
    if issubclass(user.__class__, AnonymousUser):
        return "Anonymous"
    return user.generate_token()


@register.simple_tag
def user_phone(user):
    if issubclass(user.__class__, AnonymousUser):
        return "Anonymous"

    code = user.phone_number[1]
    first = user.phone_number[1:4]
    second = user.phone_number[4:7]
    third = user.phone_number[7:]
    return f"+{code} ({first}) {second} {third}"


@register.filter(name="add_attr")
def add_attribute(field, css):
    attrs = {}
    definition = css.split(",")

    for d in definition:
        if ":" not in d:
            attrs["class"] = d
        else:
            key, val = d.split(":")
            attrs[key] = val

    return field.as_widget(attrs=attrs)
