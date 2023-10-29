from django.core import validators
from django.db import models


class ColorField(models.CharField):
    """ColorField model"""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 7)
        kwargs.setdefault("default", "#000000")
        super(ColorField, self).__init__(*args, **kwargs)
        self.validators.append(
            validators.RegexValidator(r"#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$")
        )
