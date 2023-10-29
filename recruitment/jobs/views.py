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
