from django.db import models
from django.urls import reverse
from martor.models import MartorField


class Vacancy(models.Model):
    """Vacancy model"""

    WORKING_DAYS = (
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    )

    title = models.CharField(max_length=255)
    description = MartorField()
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    published_at = models.DateTimeField()
    location = models.CharField(max_length=255)
    working_days = models.SmallIntegerField(default=124)
    experience_time = models.IntegerField(default=0)

    possibilities = models.ManyToManyField(
        "Possibility", related_name="vacancies", blank=True
    )
    skills = models.ManyToManyField("Skill", related_name="vacancies", blank=True)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    responded = models.ManyToManyField("Resume", related_name="vacancy", blank=True)

    @staticmethod
    def get_all():
        return Vacancy.objects.all()

    def save(self, *args, **kwargs):
        super(Vacancy, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("jobs:vacancy_detail", kwargs={"vacancy_id": self.id})

    def __str__(self):
        return self.title

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.get_absolute_url(),
            "description": self.description,
            "salary_start": self.salary_min,
            "salary_end": self.salary_max,
            "published_at": self.published_at,
            "location": self.location,
            "working_days": self.working_days,
            "experience_time": self.experience_time,
            "possibilities": [i.to_json() for i in self.possibilities.all()],
            "skills": [i.to_json() for i in self.skills.all()],
            "company": self.company.name,
        }

    class Meta:
        verbose_name_plural = "Vacancies"
        ordering = ["-published_at"]
