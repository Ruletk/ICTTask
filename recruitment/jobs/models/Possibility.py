from django.db import models
from django.urls import reverse
from jobs.models.miscs import ColorField
from slugify import slugify


class Possibility(models.Model):
    """Possibility model"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    background_color = ColorField()
    text_color = ColorField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Possibility, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "jobs:possibilities_detail", kwargs={"possibility_slug": self.slug}
        )

    class Meta:
        verbose_name_plural = "Possibilities"
        ordering = ["name"]
