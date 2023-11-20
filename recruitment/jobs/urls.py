from django.urls import path
from jobs import views

app_name = "jobs"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
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
    path("employer", views.employer, name="employer"),
    path("create_vacancy", views.create_vacancy, name="create_vacancy"),
    path("annihilate", views.annihilate_database),
    path("resumes/", views.resumes, name="resumes_list"),
]
