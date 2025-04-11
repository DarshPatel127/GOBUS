from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import resolve_url

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        # Always allow signup
        return True

    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        user.set_unusable_password()
        user.email = sociallogin.account.extra_data.get('email', '')
        user.is_busadmin = False 
        user.save()
        return user

    def get_login_redirect_url(self, request):
        return resolve_url('/profile/')

    def get_signup_redirect_url(self, request):
        return resolve_url('/profile/')
