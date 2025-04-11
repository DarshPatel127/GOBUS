from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import resolve_url

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_login_redirect_url(self, request):
        return resolve_url('/profile/')

    def get_signup_redirect_url(self, request):
        return resolve_url('/profile/')