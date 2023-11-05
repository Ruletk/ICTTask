from api import views
from django.urls import path


app_name = "api"

urlpatterns = [
    path(
        "switch_user_vacancy_favorite",
        views.switch_favorite_vacancy,
        name="switch_user_vacancy_favorite",
    ),
    path(
        "check_user_vacancy_favorite",
        views.check_favorite_vacancy,
        name="check_user_vacancy_favorite",
    ),
    path("switch_user_profile", views.switch_user_profile, name="switch_user_profile"),
    path("check_user_profile", views.check_user_profile, name="check_user_profile"),
]
