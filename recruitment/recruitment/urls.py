from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from recruitment import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("jobs.urls")),
    path("", include("account.urls")),
    path("api/", include("api.urls")),
    path("martor/", include("martor.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
