# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from .views import connect

from .views import alliance
from .views import alliance_create
from .views import alliance_invitations
from .views import alliance_manage
from .views import alliance_members
from .views import alliance_naps
from .views import alliance_ranks
from .views import alliance_recruitment
from .views import alliance_reports
from .views import alliance_tributes
from .views import alliance_wallet
from .views import alliance_wars
from .views import battle
from .views import battle_view
from .views import buildings
from .views import chat
from .views import commanders
from .views import fleet
from .views import fleet_trade
from .views import fleet_ships
from .views import fleet_split
from .views import fleets
from .views import fleets_handler
from .views import fleets_orbiting
from .views import fleets_ships_stats
from .views import fleets_standby
from .views import game_over
from .views import help
from .views import holidays
from .views import invasion
from .views import mails
from .views import maintenance
from .views import map
from .views import market_buy
from .views import market_sell
from .views import mercenary_intelligence
from .views import nation
from .views import notes
from .views import orbit
from .views import overview
from .views import options
from .views import planet
from .views import planets
from .views import production
from .views import ranking_alliances
from .views import ranking_players
from .views import reports
from .views import research
from .views import shipyard
from .views import spy_report
from .views import training
from .views import upkeep
from .views import start
from .views import wait



################################################################################
urlpatterns = [
	#---------------------------------------------------------------------------
	path('', RedirectView.as_view(url='/s03/connect/')),
    path('connect/', connect.View.as_view()),
	#---------------------------------------------------------------------------
    path('alliance-create/', alliance_create.View.as_view()),
    path('alliance-invitations/', alliance_invitations.View.as_view()),
    path('alliance-manage/', alliance_manage.View.as_view()),
    path('alliance-members/', alliance_members.View.as_view()),
    path('alliance-naps/', alliance_naps.View.as_view()),
    path('alliance-ranks/', alliance_ranks.View.as_view()),
    path('alliance-recruitment/', alliance_recruitment.View.as_view()),
    path('alliance-reports/', alliance_reports.View.as_view()),
    path('alliance-tributes/', alliance_tributes.View.as_view()),
    path('alliance-wallet/', alliance_wallet.View.as_view()),
    path('alliance-wars/', alliance_wars.View.as_view()),
    path('alliance/', alliance.View.as_view()),
    path('battle-view/', battle_view.View.as_view()),
    path('battle/', battle.View.as_view()),
    path('buildings/', buildings.View.as_view()),
    path('chat/', chat.View.as_view()),
    path('commanders/', commanders.View.as_view()),
    path('fleet-ships/', fleet_ships.View.as_view()),
    path('fleet-split/', fleet_split.View.as_view()),
    path('fleet-trade/', fleet_trade.View.as_view()),
    path('fleet/', fleet.View.as_view()),
    path('fleets_handler/', fleets_handler.View.as_view()),
    path('fleets-orbiting/', fleets_orbiting.View.as_view()),
    path('fleets-ships-stats/', fleets_ships_stats.View.as_view()),
    path('fleets-standby/', fleets_standby.View.as_view()),
    path('fleets/', fleets.View.as_view()),
    path('game-over/', game_over.View.as_view()),
    path('help/', help.View.as_view()),
    path('holidays/', holidays.View.as_view()),
    path('invasion/', invasion.View.as_view()),
    path('mails/', mails.View.as_view()),
    path('maintenance/', maintenance.View.as_view()),
    path('map/', map.View.as_view()),
    path('market-buy/', market_buy.View.as_view()),
    path('market-sell/', market_sell.View.as_view()),
    path('mercenary-intelligence/', mercenary_intelligence.View.as_view()),
    path('nation/', nation.View.as_view()),
    path('notes/', notes.View.as_view()),
    path('orbit/', orbit.View.as_view()),
    path('options/', options.View.as_view()),
    path('overview/', overview.View.as_view()),
    path('planets/', planets.View.as_view()),
    path('planet/', planet.View.as_view()),
    path('production/', production.View.as_view()),
    path('ranking-alliances/', ranking_alliances.View.as_view()),
    path('ranking-players/', ranking_players.View.as_view()),
    path('reports/', reports.View.as_view()),
    path('research/', research.View.as_view()),
    path('shipyard/', shipyard.View.as_view()),
    path('spy-report/', spy_report.View.as_view()),
    path('start/', start.View.as_view()),
    path('training/', training.View.as_view()),
    path('upkeep/', upkeep.View.as_view()),
    path('wait/', wait.View.as_view()),
	#---------------------------------------------------------------------------
]
################################################################################
