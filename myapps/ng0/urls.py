# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic.base import RedirectView

from .views import fleet_list
from .views import fleet_ships
from .views import fleet_split
from .views import fleet_view

from .views import home_maintenance
from .views import home_start
from .views import home_wait

from .views import mail_blacklist
from .views import mail_inbox
from .views import mail_new
from .views import mail_outbox

from .views import map

from .views import planet_buildings
from .views import planet_list
from .views import planet_orbit
from .views import planet_ships
from .views import planet_view

from .views import profile_view

from .views import report_battle
from .views import report_list

from .views import tech_list

################################################################################

urlpatterns = [

	path('', RedirectView.as_view(url='/ng0/planet-list/')),
        
    path('fleet-list/', fleet_list.View.as_view()),
    path('fleet-ships/', fleet_ships.View.as_view()),
    path('fleet-split/', fleet_split.View.as_view()),
    path('fleet-view/', fleet_view.View.as_view()),
    
    path('home-maintenance/', home_maintenance.View.as_view()),
    path('home-start/', home_start.View.as_view()),
    path('home-wait/', home_wait.View.as_view()),
    
    path('mail-blacklist/', mail_blacklist.View.as_view()),
    path('mail-inbox/', mail_inbox.View.as_view()),
    path('mail-new/', mail_new.View.as_view()),
    path('mail-outbox/', mail_outbox.View.as_view()),

    path('map/', map.View.as_view()),
    
    path('planet-buildings/', planet_buildings.View.as_view()),
    path('planet-list/', planet_list.View.as_view()),
    path('planet-orbit/', planet_orbit.View.as_view()),
    path('planet-ships/', planet_ships.View.as_view()),
    path('planet-view/', planet_view.View.as_view()),
    
    path('profile-view/', profile_view.View.as_view()),
    
    path('report-battle/', report_battle.View.as_view()),
    path('report-list/', report_list.View.as_view()),
    
    path('tech-list/', tech_list.View.as_view()),
]
