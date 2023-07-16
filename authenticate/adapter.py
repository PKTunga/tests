from allauth.account.adapter import DefaultAccountAdapter
from django.conf  import settings
from django.shortcuts import resolve_url


class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if request.user.is_admin:
            url = settings.ADMIN_LOGIN_REDIRECT_URL
        elif request.user.is_superuser:
            url = settings.SU_LOGIN_REDIRECT_URL
        else:
            url = settings.LOGIN_REDIRECT_URL
        return resolve_url(url)