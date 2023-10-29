from django.db import models
from slugify import slugify


class Company(models.Model):
    """Company model"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=255)
    logo = models.CharField(
        max_length=255
    )  # Swap it to ImageField or picture model later
    description = models.TextField()
    employee_count = models.IntegerField(default=0)
    owner = models.ForeignKey("account.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]
