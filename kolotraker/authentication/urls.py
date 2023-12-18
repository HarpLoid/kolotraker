from .views import (RegisterView, UsernameValidationView,
                    EmailValidationView, LoginView,
                    LogoutView)
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # path('', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
]
