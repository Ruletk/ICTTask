from account.models import Education
from account.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin"""


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    fields = (
        "user",
        "institution",
        "faculty",
        "speciality",
        "start_date",
        "end_date",
        "degree",
        "description",
    )
    list_display = (
        "user",
        "institution",
        "faculty",
        "speciality",
        "start_date",
        "end_date",
        "degree",
        "description",
    )
    search_fields = (
        "user",
        "institution",
        "faculty",
        "speciality",
        "start_date",
        "end_date",
        "degree",
        "description",
    )
    ordering = (
        "user",
        "institution",
        "faculty",
        "speciality",
        "start_date",
        "end_date",
        "degree",
        "description",
    )

    class Meta:
        model = Education
        fields = (
            "user",
            "university",
            "faculty",
            "specialization",
            "start_year",
            "end_year",
            "degree",
            "description",
        )
