from account import views
from django.urls import path


app_name = "account"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("profile/settings/", views.profile_settings, name="profile_settings"),
    path("profile/education/", views.profile_education, name="profile_education"),
    path("profile/security/", views.profile_security, name="profile_security"),
    path("profile/resume/", views.profile_resume, name="profile_resume"),
    path("profile/<int:id>/", views.profile_detail, name="profile_detail"),
]
