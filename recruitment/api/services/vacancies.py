import logging

from account.models import User
from jobs.models import Vacancy
from miscs.model_features import get_or_none

logger = logging.getLogger(__name__)


def switch_vacancy_user_favorites(vacancy_id: int, user: User):
    """Switching vacancy in user favorites. If on, then off, else on"""
    logger.debug("Switching vacancy user favorites: %s, %s", vacancy_id, user.username)
    vacancy = get_or_none(Vacancy, id=vacancy_id)

    if vacancy is None or user is None:
        return None

    on = False
    if vacancy in user.favorite_jobs.all():
        user.remove_favorite_job(vacancy)
    else:
        user.add_favorite_job(vacancy)
        on = True
    user.save()
    return on


def check_vacancy_user_favorites(vacancy_id: int, user: User):
    """Checking is vacancy in user favorites"""
    vacancy = get_or_none(Vacancy, id=vacancy_id)
    if vacancy is None or user is None:
        return None
    if vacancy in user.favorite_jobs.all():
        return True
    return False


def get_user_type(user: User):
    """Getting user type"""
    logger.debug("Getting user type: %s. Result: %s", user.username, user.is_employer)
    return user.is_employer


def set_user_type(user: User, rtype: bool):
    """Setting user type"""
    logger.debug("Setting user type: %s. Result: %s", user.username, rtype)
    user.is_employer = rtype
    user.save()
    return rtype
