from account.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom base user admin"""
