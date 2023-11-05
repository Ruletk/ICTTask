import datetime
import logging

from jobs.models import Vacancy
from miscs.model_features import get_or_none

logger = logging.getLogger(__name__)


def get_all_vacancies():
    logger.debug("Getting all vacancies")
    try:
        vacancies = Vacancy.objects.filter(
            published_at__lte=datetime.date.today()
        ).order_by("-id")
    except Exception as e:
        logger.error("Error while getting all vacancies: %s", e)
        vacancies = []

    return vacancies


def get_vacancies_by_filter(keyword=None, location=None, salary=None):
    logger.debug(
        "Getting vacancies by filter: keyword=%s, location=%s, salary=%s",
        keyword,
        location,
        salary,
    )
    try:
        salary = 0 if salary is None else salary * 0.8
        vacancies = Vacancy.objects.filter(
            published_at__lte=datetime.date.today(),
            title__contains=keyword,
            location__contains=location,
            salary_start__gte=salary,
        ).order_by("-id")
    except Exception as e:
        logger.error(
            "Error while getting vacancies by filter: keyword=%s, location=%s, salary=%s, error=%s",
            keyword,
            location,
            salary,
            e,
        )
        vacancies = []
    return vacancies


def get_vacancy_by_id(vacancy_id):
    logger.debug("Getting vacancy by id: %s", vacancy_id)
    vacancy = get_or_none(Vacancy, id=vacancy_id)
    return vacancy
