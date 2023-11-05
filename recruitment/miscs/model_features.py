from typing import Type

from django.db import models


def get_or_none(model: Type[models.Model], **kwargs) -> Type[models.Model] | None:
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
