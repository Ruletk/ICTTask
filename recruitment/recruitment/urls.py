from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("jobs.urls")),
    path("", include("account.urls")),
    path("api/", include("api.urls")),
    path("martor/", include("martor.urls")),
]
