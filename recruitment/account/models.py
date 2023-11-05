from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from jobs.models import Vacancy


# Create your models here.


class User(AbstractUser):
    """Custom user model"""

    phone_number = models.CharField(max_length=255)
    favorite_jobs = models.ManyToManyField("jobs.Vacancy", blank=True)
    token = models.OneToOneField(
        "Token", on_delete=models.CASCADE, related_name="user_token", null=True
    )
    is_employer = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def add_favorite_job(self, vacancy: Vacancy):
        self.favorite_jobs.add(vacancy)

    def remove_favorite_job(self, vacancy: Vacancy):
        self.favorite_jobs.remove(vacancy)

    def is_favorite_job(self, vacancy_id: int):
        return any([i.id == vacancy_id for i in self.favorite_jobs.all()])

    def generate_token(self):
        if self.token is None:
            self.token = Token.objects.create()
            self.token.generate_token()
            self.save()
        return self.token.generate_token()


class Token(models.Model):
    """JWT tokens like"""

    token = models.CharField(max_length=255)
    expired_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.token

    def is_expired(self) -> bool:
        if self.expired_at is None:
            return True
        return self.expired_at < timezone.now()

    def generate_token(self) -> str:
        """Generating new token if expired"""
        if self.is_expired() or self.token is None:
            self.token = uuid4().hex
            self.expired_at = timezone.now() + timezone.timedelta(days=1)
            self.save()
        return self.token

    @staticmethod
    def find_user(token) -> User | None:
        try:
            return Token.objects.get(token=token).user_token
        except Token.DoesNotExist:
            return None
