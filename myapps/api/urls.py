from django.urls import path, include

from myapps.api import views


urlpatterns = [

    path('', include('dj_rest_auth.urls')),

    path('allauth/', include('allauth.urls'), name='socialaccount_signup'),
    
    path('registration/', include('dj_rest_auth.registration.urls')),

    path('reset-password/<uidb64>/<token>/', views.reset_password, name='password_reset_confirm'),
    path('confirm-account/<token>/', views.confirm_account, name='account_confirm_email'),
    
    path('profile/', views.Profile.as_view()),
    
    path('home-start/', views.HomeStart.as_view()),
    
    path('layout/', views.Layout.as_view()),
]
