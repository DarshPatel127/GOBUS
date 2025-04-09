"""
URL configuration for P2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.shortcuts import redirect
from users import views as user_views
from users.views import send_otp, verify_otp
from exp.busadmin import busadmin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('busadmin/', busadmin_site.urls),
    path('', include('exp.urls')),
    path('register/', user_views.register, name="register"),
    path('profile/', user_views.profile, name="profile"),
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('accounts/',include('allauth.urls')),
    #path('accounts/3rdparty/signup/', lambda request: redirect('https://accounts.google.com/o/oauth2/auth'),name='google-login'),
    path('send-otp/', send_otp, name='send_otp'),
    path('otp_verification/', verify_otp, name='otp_verification'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
