import logging
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from jobs.models import Vacancy


# Create your models here.

logger = logging.getLogger(__name__)


def user_avatar_path(instance, filename):
    return f"avatars/{instance.id}/avatar.{filename.split('.')[-1]}"


class User(AbstractUser):
    """Custom user model"""

    patronymic = models.CharField(max_length=255, blank=True)

    avatar = models.ImageField(
        upload_to=user_avatar_path, blank=True, default="avatars/0/avatar.webp"
    )
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    favorite_jobs = models.ManyToManyField("jobs.Vacancy", blank=True)
    token = models.OneToOneField(
        "Token", on_delete=models.CASCADE, related_name="user_token", null=True
    )
    is_employer = models.BooleanField(default=False)

    user_site = models.CharField(max_length=255, blank=True)
    user_github = models.CharField(max_length=255, blank=True)
    user_twitter = models.CharField(max_length=255, blank=True)
    user_instagram = models.CharField(max_length=255, blank=True)
    user_facebook = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username

    def add_favorite_job(self, vacancy: Vacancy):
        self.favorite_jobs.add(vacancy)

    def remove_favorite_job(self, vacancy: Vacancy):
        self.favorite_jobs.remove(vacancy)

    def is_favorite_job(self, vacancy_id: int):
        for i in self.favorite_jobs.all():
            if i.id == vacancy_id:
                return True
        return False

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
        except Exception as ex:
            logger.warning(ex)


class Education(models.Model):
    """Education model"""

    DEGREES = (
        ("bachelor", "Bachelor"),
        ("master", "Master"),
        ("doctor", "Doctor"),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="education"
    )
    institution = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    degree = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.institution} - {self.faculty}"
