from account.models import User
from django.test import TestCase


class UserTestCase(TestCase):
    def test_create_user(self):
        userdata = {
            "username": "testCreateUser",
            "email": "testCreateUser@admin.com",
            "password": "testCreateUser",
        }
        user = User(**userdata)
        user.set_password(userdata["password"])
        user.save()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, userdata["username"])
        self.assertEqual(user.email, userdata["email"])
        self.assertTrue(user.check_password(userdata["password"]))

    def test_create_staff(self):
        userdata = {
            "username": "testCreateStaff",
            "email": "testCreateStaff@admin.com",
            "password": "testCreateStaff",
            "is_staff": True,
        }

        user = User(**userdata)
        user.set_password(userdata["password"])
        user.save()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, userdata["username"])
        self.assertEqual(user.email, userdata["email"])
        self.assertTrue(user.check_password(userdata["password"]))
        self.assertTrue(user.is_staff)

    def test_create_superuser(self):
        userdata = {
            "username": "testCreateSuperuser",
            "email": "testCreateSuperuser@admin.com",
            "password": "testCreateSuperuser",
            "is_staff": True,
            "is_superuser": True,
        }

        user = User(**userdata)
        user.set_password(userdata["password"])
        user.save()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, userdata["username"])
        self.assertEqual(user.email, userdata["email"])
        self.assertTrue(user.check_password(userdata["password"]))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_without_username(self):
        userdata = {
            "username": "",
            "email": "testUser@admin.com",
            "password": "testUser",
        }
        user = User(**userdata)
        user.set_password(userdata["password"])
        user.save()

        print(user.id)
        print(user.username)
        print(user.email)

        raise NotImplementedError
