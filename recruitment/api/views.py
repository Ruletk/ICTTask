import logging

from api.services.vacancies import check_vacancy_user_favorites
from api.services.vacancies import get_user_type
from api.services.vacancies import set_user_type
from api.services.vacancies import switch_vacancy_user_favorites
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from miscs.decorators import check_token
from miscs.decorators import post_only


# Create your views here.

logger = logging.getLogger(__name__)


@csrf_exempt
@post_only
@check_token
def switch_favorite_vacancy(request):
    """Body:
    "vacancy_id": id of vacancy
    """

    vacancy_id = request.json_data.get("vacancy_id", None)
    if not vacancy_id:
        logger.info("invalid request for %s, %s", request.user, vacancy_id)
        return JsonResponse({"status": "error", "message": "invalid request"})

    res = switch_vacancy_user_favorites(vacancy_id, request.user)
    if res is None:
        return JsonResponse(
            {"status": "error", "message": "invalid vacancy id or user id"}
        )

    return JsonResponse({"status": "ok", "message": "success", "on": res})


@csrf_exempt
@post_only
@check_token
def check_favorite_vacancy(request):
    """Body:
    "vacancy_id": id of vacancy
    """
    vacancy_id = request.json_data.get("vacancy_id", None)

    if vacancy_id is None:
        logger.info("invalid request for %s, %s", request.user, vacancy_id)
        return JsonResponse({"status": "error", "message": "invalid request"})

    res = check_vacancy_user_favorites(vacancy_id, request.user)
    if res is None:
        return JsonResponse(
            {"status": "error", "message": "invalid vacancy id or user id"}
        )
    return JsonResponse({"status": "ok", "message": "success", "on": res})


@csrf_exempt
@post_only
@check_token
def check_user_profile(request):
    res = get_user_type(request.user)
    return JsonResponse({"status": "ok", "message": "success", "type": res})


@csrf_exempt
@post_only
@check_token
def switch_user_profile(request):
    typ = request.json_data.get("type", None)
    if typ is None:
        return JsonResponse(
            {"status": "error", "message": "invalid request. type must be in request"}
        )
    if typ:
        messages.info(request, "You are now employer")
    else:
        messages.info(request, "You are now employee")
    res = set_user_type(request.user, typ)
    return JsonResponse({"status": "ok", "message": "success", "type": res})
