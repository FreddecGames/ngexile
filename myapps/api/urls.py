from django.urls import path, include

from myapps.api.views import reset_password, confirm_account


urlpatterns = [

    path('', include('dj_rest_auth.urls')),

    path('allauth/', include('allauth.urls'), name='socialaccount_signup'),
    
    path('registration/', include('dj_rest_auth.registration.urls')),

    path('reset-password/<uidb64>/<token>/', reset_password, name='password_reset_confirm'),
    path('confirm-account/<token>/', confirm_account, name='account_confirm_email'),
]
