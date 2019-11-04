from django.urls import path, re_path
from . import views as auth_views
from django.contrib.auth import views as django_auth_views

urlpatterns = (
    # Login logout urls
    re_path(r'^login/$', django_auth_views.LoginView.as_view(
        template_name='authentication/login.html'
    ), name='login'),
    re_path(r'^logout/$', django_auth_views.LogoutView.as_view(
        template_name='authentication/logged_out.html'
    ), name='logout'),

    # Reset accounts urls
    path('password_reset/', django_auth_views.PasswordResetView.as_view(
        email_template_name='authentication/password_reset_email.html',
        subject_template_name='authentication/password_reset_subject.txt',
        template_name='authentication/password_reset_form.html'
    ), name='password_reset'),
    path('password_reset/done/', django_auth_views.PasswordResetDoneView.as_view(
        template_name='authentication/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', django_auth_views.PasswordResetConfirmView.as_view(
        template_name='authentication/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', django_auth_views.PasswordResetCompleteView.as_view(
        template_name='authentication/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Create new account url
    re_path(r'^register/$', auth_views.UserRegisterView.as_view(), name='register')
)
