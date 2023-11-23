import logging

from django.core.paginator import EmptyPage
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from jobs.forms import CreateVacancyForm
from jobs.services.vacancies import get_all_vacancies
from jobs.services.vacancies import get_vacancies_by_filter
from jobs.services.vacancies import get_vacancies_by_possibility
from jobs.services.vacancies import get_vacancy_by_id
from miscs.decorators import employer_only
from miscs.decorators import worker_only

# Create your views here.

logger = logging.getLogger(__name__)


@worker_only
def index(request):
    vacancies = get_all_vacancies()[:20]
    context = {"vacancies": vacancies}
    return render(request, "jobs/index.html", context)


@worker_only
def vacancy_detail(request, vacancy_id):
    vacancies = get_vacancy_by_id(vacancy_id)
    context = {"vacancy": vacancies}
    return render(request, "jobs/vacancy_detail.html", context)


def possibilities_detail(request, possibility_slug):
    vacancies = get_vacancies_by_possibility(possibility_slug)
    context = {"vacancies": vacancies}
    return render(request, "jobs/possibilities_detail.html", context)


def search(request):
    query, location, salary, page, only_favorites = (
        request.GET.get("query", ""),
        request.GET.get("location", ""),
        request.GET.get("salary", 0),
        request.GET.get("page", 1),
        request.GET.get("favorite", False),
    )
    try:
        vacancies = get_vacancies_by_filter(
            request.user, query, location, salary, page, only_favorites
        )
    except EmptyPage:
        return HttpResponse("")
    context = {"vacancies": vacancies.object_list}
    if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        return render(request, "snippets/vacancy_card.html", context)
    return render(request, "jobs/search.html", context)


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


@employer_only
def create_vacancy(request):
    if request.method == "GET":
        form = CreateVacancyForm()
        return render(request, "jobs/create_vacancy.html", {"form": form})
    form = CreateVacancyForm(request.POST)
    if form.is_valid():
        form.user = request.user
        vacancy = form.save(commit=True)

        return HttpResponseRedirect(reverse("jobs:vacancy_detail", args=[vacancy.id]))
    print(form.errors)
    return render(request, "jobs/create_vacancy.html", {"form": form})


def annihilate_database(request):
    if request.user.id != 1:
        return redirect("/")
    from django.db.transaction import atomic

    with atomic():
        ...
        logger.debug("Database annihilated")


def resumes(request):
    return render(request, "jobs/resumes_list.html")
