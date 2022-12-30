from django.urls import path

from .views import alliance_overview
from .views import commander_overview
from .views import fleet_overview
from .views import game_start
from .views import mail_inbox
from .views import map_galaxy
from .views import planet_buildings
from .views import profile_overview
from .views import ranking_player


urlpatterns = [
    
    path('alliance_overview/', alliance_overview.View.as_view()),
    
    path('commander_overview/', commander_overview.View.as_view()),
    
    path('fleet_overview/', fleet_overview.View.as_view()),
    
    path('game_start/', game_start.View.as_view()),
    
    path('mail_inbox/', mail_inbox.View.as_view()),
    
    path('map_galaxy/', map_galaxy.View.as_view()),

    path('planet_buildings/', planet_buildings.View.as_view()),

    path('profile_overview/', profile_overview.View.as_view()),
    
    path('ranking_player/', ranking_player.View.as_view()),
    
    path('', profile_overview.View.as_view()),
]
