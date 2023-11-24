from account.forms import PasswordChangeForm
from account.forms import UserEducationForm
from account.forms import UserSecurityForm
from account.forms import UserSettingsForm
from account.models import User


def change_password(user: User, password_form: PasswordChangeForm) -> User:
    """
    Change user password. Logic of this function is in PasswordChangeForm
    in save method.

    @param user: Input user, in many cases is request.user
    @param password_form: Password form, only UserSecurityForm
    @return: User
    """
    password_form.instance = user
    return password_form.save()


def change_security(user: User, form: UserSecurityForm) -> User:
    """
    Change user security settings. Logic of this function is in UserSecurityForm
    in save method.

    @param user: Input user, in many cases is request.user
    @param form: Change user security form, only UserSecurityForm
    @return: User
    """
    form.instance = user
    return form.save()


def change_education(user: User, form: UserEducationForm) -> User:
    """
    Change user education. Logic of this function is in UserEducationForm
    in save method.

    @param user: Input user, in many cases is request.user
    @param form: Change user education form, only UserEducationForm
    @return: User
    """
    form.instance = user
    return form.save()


def change_settings(user: User, form: UserSettingsForm, files) -> User:
    """
    Change user settings. Logic of this function is in UserSettingsForm
    in save method.

    @param user: Input user, in many cases is request.user
    @param form: Change user settings form, only UserSettingsForm
    @param files: Files from request.FILES
    @return: User
    """
    form.instance = user
    if files.get("avatar"):
        user.avatar.delete()
        user.avatar = files.get("avatar")
    return form.save()
