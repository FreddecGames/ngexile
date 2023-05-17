# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic.base import RedirectView

from .views import empire_view

from .views import home_maintenance
from .views import home_start

################################################################################

urlpatterns = [
    
	path('', RedirectView.as_view(url='/ng0/empire-view')),

    path('empire-view/', empire_view.View.as_view()),
    
    path('home-maintenance/', home_maintenance.View.as_view()),
    path('home-start/', home_start.View.as_view()),
]
