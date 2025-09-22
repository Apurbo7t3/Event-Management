from django.urls import path
from core.views import sign_in,user_login,sign_out,no_access
urlpatterns = [
    path('sign-in/',sign_in,name='sign-in'),
    path('sign-out/',sign_out,name='sign-out'),
    path('login-page/',user_login,name='login-page'),
    path('no-access/',no_access,name='no-access'),
]
