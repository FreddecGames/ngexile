from django.urls import path
from django.views.generic.base import RedirectView

from .views import connect

from .views import empire_planets
from .views import empire_purchases
from .views import empire_sales
from .views import empire_view

from .views import fleet_list
from .views import fleet_ships
from .views import fleet_split
from .views import fleet_view

from .views import home_gameover
from .views import home_maintenance
from .views import home_start
from .views import home_wait

from .views import map_galaxy
from .views import map_sector
from .views import map_universe

from .views import planet_buildings
from .views import planet_ships
from .views import planet_orbit
from .views import planet_trainings
from .views import planet_view

from .views import ranking_player

from .views import report_battle
from .views import report_list

from .views import tech_list

urlpatterns = [
    
	path('connect/', connect.View.as_view()),
    
	path('empire-planets/', empire_planets.View.as_view()),
	path('empire-purchases/', empire_purchases.View.as_view()),
	path('empire-sales/', empire_sales.View.as_view()),
	path('empire-view/', empire_view.View.as_view()),
    
	path('fleet-list/', fleet_list.View.as_view()),
	path('fleet-ships/', fleet_ships.View.as_view()),
	path('fleet-split/', fleet_split.View.as_view()),
	path('fleet-view/', fleet_view.View.as_view()),

	path('home-gameover/', home_gameover.View.as_view()),
	path('home-maintenance/', home_maintenance.View.as_view()),
	path('home-start/', home_start.View.as_view()),
	path('home-wait/', home_wait.View.as_view()),

	path('map-galaxy/', map_galaxy.View.as_view()),
	path('map-sector/', map_sector.View.as_view()),
	path('map-universe/', map_universe.View.as_view()),

	path('planet-buildings/', planet_buildings.View.as_view()),
	path('planet-ships/', planet_ships.View.as_view()),
	path('planet-orbit/', planet_orbit.View.as_view()),
	path('planet-trainings/', planet_trainings.View.as_view()),
	path('planet-view/', planet_view.View.as_view()),
    
	path('ranking-player/', ranking_player.View.as_view()),
    
	path('report-battle/', report_battle.View.as_view()),
	path('report-list/', report_list.View.as_view()),
    
	path('tech-list/', tech_list.View.as_view()),
    
	path('', RedirectView.as_view(url='/ng0/connect')),
]
