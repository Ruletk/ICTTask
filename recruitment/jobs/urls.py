from django.urls import path
from jobs import views


app_name = "jobs"

urlpatterns = [
    path("", views.index, name="index"),
    path("vacancy/<int:vacancy_id>", views.vacancy_detail, name="vacancy_detail"),
    path(
        "possibilities/<slug:possibility_slug>",
        views.possibilities_detail,
        name="possibilities_detail",
    ),
    path(
        "vacancies/<int:pagination_page>", views.vacancies_list, name="vacancies_list"
    ),
    path("jobs/<int:pagination_page>", views.jobs_list, name="jobs_list"),
    path(
        "companies/<int:pagination_page>", views.companies_list, name="companies_list"
    ),
    path("blog/<int:pagination_page>", views.blog_list, name="blog_list"),
]
