from account import views
from django.urls import path


app_name = "account"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("profile/<str:username>/", views.profile_detail, name="profile_detail"),
]
