from django.urls import path, include

from .views import redirection

from .views import profile

from .views import home_start

from .views import layout


urlpatterns = [

    path('', include('dj_rest_auth.urls')),

    path('allauth/', include('allauth.urls'), name='socialaccount_signup'),
    
    path('registration/', include('dj_rest_auth.registration.urls')),

    path('reset-password/<uidb64>/<token>/', redirection.reset_password, name='password_reset_confirm'),
    path('confirm-account/<token>/', redirection.confirm_account, name='account_confirm_email'),
    
    path('profile/', profile.View.as_view()),
    
    path('home-start/', home_start.View.as_view()),
    
    path('layout/', layout.View.as_view()),
]
