from django.urls import path
from core.views import sign_in,user_login,sign_out,no_access,EditProfileView,PassChangeView,PassResetView,PassResetConfirmView
from django.contrib.auth.views import PasswordChangeDoneView,LogoutView
urlpatterns = [
    path('sign-in/',sign_in,name='sign-in'),
    path('sign-out/',sign_out,name='sign-out'),
    path('login-page/',user_login,name='login-page'),
    path('no-access/',no_access,name='no-access'),
    path('edit-profile/',EditProfileView.as_view(),name='edit-profile'),
    path('password-change/',PassChangeView.as_view(),name='password-change'),
    path('password-change/done/',PasswordChangeDoneView.as_view(template_name='profile.html'),name='password_change_done'),
    path('password-reset/',PassResetView.as_view(),name='password-reset'),
    path('password-reset/confirm/<uidb64>/<token>/',PassResetConfirmView.as_view(),name='password_reset_confirm'),
]
