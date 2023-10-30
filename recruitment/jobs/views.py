from django.shortcuts import render
from jobs.services.vacancies import get_all_vacancies
from jobs.services.vacancies import get_vacancy_by_id

# Create your views here.


def index(request):
    vacancies = get_all_vacancies()
    context = {"vacancies": vacancies}
    return render(request, "jobs/index.html", context)


def vacancy_detail(request, vacancy_id):
    vacancy = get_vacancy_by_id(vacancy_id)
    context = {"vacancy": vacancy}
    return render(request, "jobs/vacancy_detail.html", context)


def possibilities_detail(request, possibility_slug):
    return render(request, "jobs/possibilities_detail.html")


def vacancies_list(request, pagination_page=1):
    return render(request, "jobs/vacancies_list.html")


def jobs_list(request, pagination_page=1):
    return render(request, "jobs/jobs_list.html")


def companies_list(request, pagination_page=1):
    return render(request, "jobs/companies_list.html")


def blog_list(request, pagination_page=1):
    return render(request, "jobs/blog_list.html")
