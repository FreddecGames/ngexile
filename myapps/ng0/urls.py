from django.urls import path
from django.views.generic.base import RedirectView

from .views import empire_view

from .views import map_galaxy
from .views import map_sector
from .views import map_universe

urlpatterns = [

	path('empire-view/', empire_view.View.as_view()),

	path('map-galaxy/', map_galaxy.View.as_view()),
	path('map-sector/', map_sector.View.as_view()),
	path('map-universe/', map_universe.View.as_view()),
    
	path('', RedirectView.as_view(url='/ng0/empire-view')),
]
