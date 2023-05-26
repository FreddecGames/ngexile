# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic.base import RedirectView

from .views import home_gameover
from .views import home_maintenance
from .views import home_start
from .views import home_wait

from .views import planet_list
from .views import planet_view

################################################################################

urlpatterns = [

	path('', RedirectView.as_view(url='/ng0/planet-list/')),
    
    path('home-gameover/', home_gameover.View.as_view()),
    path('home-maintenance/', home_maintenance.View.as_view()),
    path('home-start/', home_start.View.as_view()),
    path('home-wait/', home_wait.View.as_view()),
    
    path('planet-list/', planet_list.View.as_view()),
    path('planet-view/', planet_view.View.as_view()),
]
