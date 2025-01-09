# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic.base import RedirectView

from .views import home_maintenance
from .views import home_start

from .views import planet_buildings

################################################################################

urlpatterns = [

	path('', RedirectView.as_view(url='/s04/planet-buildings/')),

    path('home-maintenance/', home_maintenance.View.as_view()),
    path('home-start/', home_start.View.as_view()),

    path('planet-buildings/', planet_buildings.View.as_view()),
]

