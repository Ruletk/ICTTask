from django.urls import path
from jobs import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("vacancies/", views.vacancies, name="vacancies"),
    path("vacancy/<int:vacancy_id>", views.vacancy_detail, name="vacancy_detail"),
]
