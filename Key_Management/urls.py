"""
URL configuration for Key_Management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_view
from users import views as users_view
from django.views.generic import TemplateView
from users.loginBackend import CustomLoginView


urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', include('base.urls')), 
    path('register/', users_view.register, name='register'),
    path('login/', CustomLoginView.as_view(template_name = 'users/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name = 'users/password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'), name='password_reset_complete'),
    path('confirm-email/<uidb64>/<token>/', users_view.confirm_email, name='confirm_email'),
    path('email-confirmed/', TemplateView.as_view(template_name='users/email_confirmed.html'), name='email_confirmed'),
    path('email-confirmation-invalid/', TemplateView.as_view(template_name='users/email_confirmation_invalid.html'), name='email_confirmation_invalid'),
    path('email-confirmation-sent/', TemplateView.as_view(template_name='users/email_confirmation_sent.html'), name='email_confirmation_sent'),
]
