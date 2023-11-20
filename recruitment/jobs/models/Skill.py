from django.db import models
from slugify import slugify


class Skill(models.Model):
    """Skill model"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Skill, self).save(*args, **kwargs)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
        }

    class Meta:
        verbose_name_plural = "Skills"
        ordering = ["name"]
