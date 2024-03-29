# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic.base import RedirectView

from .views import alliance_create
from .views import alliance_invitations
from .views import alliance_manage
from .views import alliance_members
from .views import alliance_naps
from .views import alliance_ranks
from .views import alliance_recruitment
from .views import alliance_reports
from .views import alliance_tributes
from .views import alliance_view
from .views import alliance_wallet
from .views import alliance_wars

from .views import chat

from .views import commander_edit
from .views import commander_list

from .views import empire_orbiting
from .views import empire_planets
from .views import empire_standby
from .views import empire_stats
from .views import empire_upkeep
from .views import empire_view

from .views import fleet_list
from .views import fleet_ships
from .views import fleet_split
from .views import fleet_view

from .views import help

from .views import home_gameover
from .views import home_holidays
from .views import home_start
from .views import home_wait

from .views import mail_blacklist
from .views import mail_inbox
from .views import mail_new
from .views import mail_outbox

from .views import maintenance

from .views import map

from .views import market_buy
from .views import market_sell

from .views import mercenary

from .views import planet_buildings
from .views import planet_orbit
from .views import planet_production
from .views import planet_recycling
from .views import planet_ships
from .views import planet_trainings
from .views import planet_transferts
from .views import planet_view
from .views import planet_working

from .views import profile_notes
from .views import profile_options
from .views import profile_view

from .views import ranking_alliances
from .views import ranking_players

from .views import report_battle
from .views import report_invasion
from .views import report_list
from .views import report_spy

from .views import tech_list

################################################################################

urlpatterns = [

	path('', RedirectView.as_view(url='/s03/empire-view/')),
    
    path('alliance-create/', alliance_create.View.as_view()),
    path('alliance-invitations/', alliance_invitations.View.as_view()),
    path('alliance-manage/', alliance_manage.View.as_view()),
    path('alliance-members/', alliance_members.View.as_view()),
    path('alliance-naps/', alliance_naps.View.as_view()),
    path('alliance-ranks/', alliance_ranks.View.as_view()),
    path('alliance-recruitment/', alliance_recruitment.View.as_view()),
    path('alliance-reports/', alliance_reports.View.as_view()),
    path('alliance-tributes/', alliance_tributes.View.as_view()),
    path('alliance-view/', alliance_view.View.as_view()),
    path('alliance-wallet/', alliance_wallet.View.as_view()),
    path('alliance-wars/', alliance_wars.View.as_view()),
    
    path('chat/', chat.View.as_view()),
    
    path('commander-edit/', commander_edit.View.as_view()),
    path('commander-list/', commander_list.View.as_view()),
    
    path('empire-orbiting/', empire_orbiting.View.as_view()),
    path('empire-planets/', empire_planets.View.as_view()),
    path('empire-stats/', empire_stats.View.as_view()),
    path('empire-standby/', empire_standby.View.as_view()),
    path('empire-upkeep/', empire_upkeep.View.as_view()),
    path('empire-view/', empire_view.View.as_view()),
    
    path('fleet-list/', fleet_list.View.as_view()),
    path('fleet-ships/', fleet_ships.View.as_view()),
    path('fleet-split/', fleet_split.View.as_view()),
    path('fleet-view/', fleet_view.View.as_view()),
    
    path('help/', help.View.as_view()),
    
    path('home-gameover/', home_gameover.View.as_view()),
    path('home-holidays/', home_holidays.View.as_view()),
    path('home-start/', home_start.View.as_view()),
    path('home-wait/', home_wait.View.as_view()),
    
    path('mail-blacklist/', mail_blacklist.View.as_view()),
    path('mail-inbox/', mail_inbox.View.as_view()),
    path('mail-new/', mail_new.View.as_view()),
    path('mail-outbox/', mail_outbox.View.as_view()),
    
    path('maintenance/', maintenance.View.as_view()),

    path('map/', map.View.as_view()),
   
    path('market-buy/', market_buy.View.as_view()),
    path('market-sell/', market_sell.View.as_view()),
    
    path('mercenary/', mercenary.View.as_view()),
    
    path('planet-buildings/', planet_buildings.View.as_view()),
    path('planet-orbit/', planet_orbit.View.as_view()),
    path('planet-production/', planet_production.View.as_view()),
    path('planet-recycling/', planet_recycling.View.as_view()),
    path('planet-ships/', planet_ships.View.as_view()),
    path('planet-trainings/', planet_trainings.View.as_view()),
    path('planet-transferts/', planet_transferts.View.as_view()),
    path('planet-view/', planet_view.View.as_view()),
    path('planet-working/', planet_working.View.as_view()),
    
    path('profile-notes/', profile_notes.View.as_view()),
    path('profile-options/', profile_options.View.as_view()),
    path('profile-view/', profile_view.View.as_view()),
    
    path('ranking-alliances/', ranking_alliances.View.as_view()),
    path('ranking-players/', ranking_players.View.as_view()),
    
    path('report-battle/', report_battle.View.as_view()),
    path('report-invasion/', report_invasion.View.as_view()),    
    path('report-list/', report_list.View.as_view()),
    path('report-spy/', report_spy.View.as_view()),
    
    path('tech-list/', tech_list.View.as_view()),
]
