from django.db import models
from martor.models import MartorField
from slugify import slugify


class Company(models.Model):
    """Company model"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=255)
    logo = models.CharField(
        max_length=255
    )  # Swap it to ImageField or picture model later
    description = MartorField()
    employee_count = models.IntegerField(default=0)
    owner = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="company"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "location": self.location,
            "logo": self.logo,
            "description": self.description,
            "employee_count": self.employee_count,
            "owner": self.owner.username,
        }

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]
