from django.db import models
from django.urls import reverse


class Vacancy(models.Model):
    """Vacancy model"""

    title = models.CharField(max_length=255)
    description = models.TextField()
    salary_start = models.FloatField()
    salary_end = models.FloatField()
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    published_at = models.DateField()
    location = models.CharField(max_length=255)
    date_work = models.IntegerField(default=0)
    skill_time = models.IntegerField(default=0)

    possibilities = models.ManyToManyField(
        "Possibility", related_name="vacancies", blank=True
    )
    skills = models.ManyToManyField("Skill", related_name="vacancies", blank=True)

    @staticmethod
    def get_all():
        return Vacancy.objects.all()

    def save(self, *args, **kwargs):
        super(Vacancy, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("jobs:vacancy_detail", kwargs={"vacancy_id": self.id})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Vacancies"
        ordering = ["title"]
