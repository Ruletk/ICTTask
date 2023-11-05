import logging

from django.shortcuts import render
from jobs.forms import SearchJobForm
from jobs.services.vacancies import get_all_vacancies
from jobs.services.vacancies import get_vacancies_by_filter
from jobs.services.vacancies import get_vacancy_by_id
from miscs.decorators import employer_only
from miscs.decorators import worker_only

# Create your views here.

logger = logging.getLogger(__name__)


@worker_only
def index(request):
    if request.method == "GET":
        vacancies = get_all_vacancies()
        context = {"vacancies": vacancies}
        return render(request, "jobs/index.html", context)
    form = SearchJobForm(request.POST)
    if form.is_valid():
        keyword, location, salary = (
            form.cleaned_data["keyword"],
            form.cleaned_data["location"],
            form.cleaned_data["salary"],
        )
        vacancies = get_vacancies_by_filter(keyword, location, salary)
        context = {
            "vacancies": vacancies,
            "search_query": {
                "keyword": keyword,
                "location": location,
                "salary": salary if salary else 0,
            },
        }
    else:
        context = {"vacancies": []}
    return render(request, "jobs/index.html", context)


@worker_only
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


@employer_only
def employer(request):
    return render(request, "jobs/employer.html")
