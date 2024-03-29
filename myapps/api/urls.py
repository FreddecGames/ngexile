from django.urls import path, include

from .views import redirection

from .views import user

from .views import home_gameover
from .views import home_holidays
from .views import home_start
from .views import home_wait

from .views import layout

from .views import alliance_create
from .views import alliance_gift
from .views import alliance_invitations
from .views import alliance_manage
from .views import alliance_members
from .views import alliance_naps
from .views import alliance_ranks
from .views import alliance_recruitment
from .views import alliance_reports
from .views import alliance_request
from .views import alliance_tag
from .views import alliance_tax
from .views import alliance_tributes
from .views import alliance_view
from .views import alliance_wallet
from .views import alliance_wars

from .views import chat_new
from .views import chat_view

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

from .views import help_buildings
from .views import help_ships
from .views import help_techs

from .views import mail_blacklist
from .views import mail_inbox
from .views import mail_new
from .views import mail_outbox

from .views import map_galaxy
from .views import map_sector
from .views import map_universe

from .views import market_buy
from .views import market_sell

from .views import mercenary_planet
from .views import mercenary_player

from .views import planet_buildings
from .views import planet_buy
from .views import planet_change
from .views import planet_orbit
from .views import planet_production
from .views import planet_recycling
from .views import planet_sell
from .views import planet_ships
from .views import planet_trainings
from .views import planet_transferts
from .views import planet_view
from .views import planet_working

from .views import profile_edit
from .views import profile_holidays
from .views import profile_notes
from .views import profile_options
from .views import profile_user
from .views import profile_view

from .views import ranking_alliances
from .views import ranking_players

from .views import report_battle
from .views import report_invasion
from .views import report_list
from .views import report_spy

from .views import tech_list


urlpatterns = [

    path('', include('dj_rest_auth.urls')),

    path('allauth/', include('allauth.urls'), name='socialaccount_signup'),
    
    path('registration/', include('dj_rest_auth.registration.urls')),

    path('reset-password/<uidb64>/<token>/', redirection.reset_password, name='password_reset_confirm'),
    path('confirm-account/<token>/', redirection.confirm_account, name='account_confirm_email'),
    
    path('user/', user.View.as_view()),
    
    path('home-gameover/', home_gameover.View.as_view()),
    path('home-holidays/', home_holidays.View.as_view()),
    path('home-start/', home_start.View.as_view()),
    path('home-wait/', home_wait.View.as_view()),
    
    path('layout/', layout.View.as_view()),
    
    path('alliance-create/', alliance_create.View.as_view()),
    path('alliance-gift/', alliance_gift.View.as_view()),
    path('alliance-invitations/', alliance_invitations.View.as_view()),
    path('alliance-manage/', alliance_manage.View.as_view()),
    path('alliance-members/', alliance_members.View.as_view()),
    path('alliance-naps/', alliance_naps.View.as_view()),
    path('alliance-ranks/', alliance_ranks.View.as_view()),
    path('alliance-recruitment/', alliance_recruitment.View.as_view()),
    path('alliance-reports/', alliance_reports.View.as_view()),
    path('alliance-request/', alliance_request.View.as_view()),
    path('alliance-tag/<slug:tag>/', alliance_tag.View.as_view()),
    path('alliance-tax/', alliance_tax.View.as_view()),
    path('alliance-tributes/', alliance_tributes.View.as_view()),
    path('alliance-view/', alliance_view.View.as_view()),
    path('alliance-wallet/', alliance_wallet.View.as_view()),
    path('alliance-wars/', alliance_wars.View.as_view()),
    
    path('chat/<int:id>/', chat_view.View.as_view()),
    path('chat-new/', chat_new.View.as_view()),
    
    path('commander-edit/<int:id>/', commander_edit.View.as_view()),
    path('commander-list/', commander_list.View.as_view()),
    
    path('empire-orbiting/', empire_orbiting.View.as_view()),
    path('empire-planets/', empire_planets.View.as_view()),
    path('empire-standby/', empire_standby.View.as_view()),
    path('empire-stats/', empire_stats.View.as_view()),
    path('empire-upkeep/', empire_upkeep.View.as_view()),
    path('empire-view/', empire_view.View.as_view()),
    
    path('fleet-list/', fleet_list.View.as_view()),
    path('fleet-ships/<int:id>/', fleet_ships.View.as_view()),
    path('fleet-split/<int:id>/', fleet_split.View.as_view()),
    path('fleet-view/<int:id>/', fleet_view.View.as_view()),
    
    path('help-buildings/', help_buildings.View.as_view()),
    path('help-ships/', help_ships.View.as_view()),
    path('help-techs/', help_techs.View.as_view()),

    path('mail-blacklist/', mail_blacklist.View.as_view()),
    path('mail-inbox/', mail_inbox.View.as_view()),
    path('mail-new/', mail_new.View.as_view()),
    path('mail-outbox/', mail_outbox.View.as_view()),

    path('map/', map_universe.View.as_view()),
    path('map/<int:galaxy>/', map_galaxy.View.as_view()),
    path('map/<int:galaxy>/<int:sector>/', map_sector.View.as_view()),
    
    path('market-buy/', market_buy.View.as_view()),
    path('market-sell/', market_sell.View.as_view()),
    
    path('mercenary-planet/', mercenary_planet.View.as_view()),
    path('mercenary-player/', mercenary_player.View.as_view()),
    
    path('planet-buildings/', planet_buildings.View.as_view()),
    path('planet-buy/', planet_buy.View.as_view()),
    path('planet-change/', planet_change.View.as_view()),
    path('planet-orbit/', planet_orbit.View.as_view()),
    path('planet-production/', planet_production.View.as_view()),
    path('planet-recycling/', planet_recycling.View.as_view()),
    path('planet-sell/', planet_sell.View.as_view()),
    path('planet-ships/', planet_ships.View.as_view()),
    path('planet-trainings/', planet_trainings.View.as_view()),
    path('planet-transferts/', planet_transferts.View.as_view()),
    path('planet-view/', planet_view.View.as_view()),
    path('planet-working/', planet_working.View.as_view()),
    
    path('profile/<int:id>/', profile_user.View.as_view()),
    path('profile-edit/', profile_edit.View.as_view()),
    path('profile-holidays/', profile_holidays.View.as_view()),
    path('profile-notes/', profile_notes.View.as_view()),
    path('profile-options/', profile_options.View.as_view()),
    path('profile-view/', profile_view.View.as_view()),
    
    path('ranking-alliances/', ranking_alliances.View.as_view()),
    path('ranking-players/', ranking_players.View.as_view()),
    
    path('report-battle/<int:id>/', report_battle.View.as_view()),
    path('report-invasion/<int:id>/', report_invasion.View.as_view()),    
    path('report-list/', report_list.View.as_view()),
    path('report-spy/<int:id>/', report_spy.View.as_view()),
    
    path('tech-list/', tech_list.View.as_view()),
]
