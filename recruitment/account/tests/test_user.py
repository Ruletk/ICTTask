from account.models import User
from django.test import TestCase


def create_user(username, email, password, **kwargs):
    user = User(username=username, email=email, **kwargs)
    user.set_password(password)
    user.save()
    return user


class UserTestCase(TestCase):
    def setUp(self):
        self.test_user = create_user(
            username="testuser", email="testuser@site.com", password="test"
        )

    def test_create_user(self):
        data = {"username": "test", "email": "test@site.com", "password": "test"}
        user = User.objects.create_user(**data)
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_get_user(self):
        self.assertEqual(self.test_user, User.objects.get(username="testuser"))
        self.assertEqual(self.test_user, User.objects.get(email="testuser@site.com"))
        self.assertEqual(self.test_user, User.objects.get(pk=self.test_user.id))
