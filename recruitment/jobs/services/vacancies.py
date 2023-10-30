import datetime

from jobs.models import Vacancy


def get_all_vacancies():
    return [
        i
        for i in Vacancy.objects.order_by("-id")
        if i.published_at <= datetime.date.today()
    ]


def get_vacancy_by_id(vacancy_id):
    return Vacancy.objects.get(id=vacancy_id)
