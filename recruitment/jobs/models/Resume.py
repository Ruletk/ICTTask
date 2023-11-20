from django.db import models


class Resume(models.Model):
    title = models.CharField(max_length=255)
    salary = models.FloatField()
    skills = models.ManyToManyField("Skill", related_name="resumes", blank=True)
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

    experience = models.TextField()
    education = models.TextField()
    achievements = models.TextField()
    hobbies = models.TextField()
    additional_info = models.TextField()

    def __str__(self):
        return self.title
