import datetime
import logging

from django.core.paginator import EmptyPage
from django.core.paginator import Page
from django.core.paginator import Paginator
from django.db.models import QuerySet
from jobs.models import Vacancy
from miscs.model_features import get_or_none

logger = logging.getLogger(__name__)


def get_all_vacancies():
    """
    Get all vacancies
    @return: QuerySet of vacancies
    """
    logger.debug("Getting all vacancies")
    try:
        vacancies = Vacancy.objects.filter(
            published_at__lte=datetime.date.today()
        ).order_by("-published_at")
    except Exception as e:
        logger.error("Error while getting all vacancies: %s", e)
        vacancies = []

    return vacancies


def get_vacancies_by_filter(
    query: str = "", location: str = "", salary: int = 0, page: int = 1
) -> Page:
    """
    Get vacancies by filter
    Output tuple where first element is list of vacancies
    and second element is dict of search query (dict of keyword, location, salary)
    for rendering the search field in the template
    @param query: String with keyword or keywords
    @param location: String with name of city
    @param salary: Integer with minimal salary
    @param page: Integer with page number
    @return: QuerySet of vacancies
    """
    logger.debug(
        "Getting vacancies by filter: keyword=%s, location=%s, salary=%s, page=%s",
        query,
        location,
        salary,
        page,
    )
    query = query.strip() if query else ""
    location = location.strip() if location else ""
    salary = int(salary) if salary else 0
    try:
        q_salary = int(salary * 0.8) if salary else -1
        vacancies = Vacancy.objects.filter(
            published_at__lte=datetime.date.today(),
            title__contains=query,
            location__contains=location,
            salary_min__gte=q_salary,
        ).order_by("-published_at")
        paginator = Paginator(vacancies, 20)
    except EmptyPage:
        raise
    except Exception as e:
        logger.error(
            "Error while getting vacancies by filter: keyword=%s, location=%s, salary=%s, error=%s",
            query,
            location,
            salary,
            e,
        )
        paginator = Paginator([], 20)
    return paginator.page(page)


def get_vacancy_by_id(vacancy_id):
    """
    Get vacancy by id
    @param vacancy_id: Integer with id of vacancy
    @rtype: Vacancy
    """
    logger.debug("Getting vacancy by id: %s", vacancy_id)
    vacancy = get_or_none(Vacancy, id=vacancy_id)
    return vacancy


def get_vacancies_by_possibility(possibility_slug) -> QuerySet:
    """
    Get vacancies by possibility
    @param possibility_slug: String with slug of possibility
    @rtype: QuerySet of vacancies
    """
    vacancies = Vacancy.objects.filter(possibilities__slug__exact=possibility_slug)
    return vacancies
