# -*- coding: utf-8 -*-

registration = {
    "enabled":True,
    "until":None
}

allowedOrientations = [1,2,3]
allowedRetry = True
allowedHolidays = True

maintenance = False            # enable/disable maintenance
maintenance_msg = "Maintenance serveur ..." #"Mise à jour logiciel ...";#"Maintenance serveur" #Migration de la base de donnée";

# Players relationships constants (pas touche !)
rUninhabited = -3
rWar = -2
rHostile = -1
rFriend = 0
rAlliance = 1
rSelf = 2

# Session constant names
sUser = "user"
sPlanet = "planet"
sPlanetList = "planetlist"
sPlanetListCount = "planetlistcount"
sPrivilege = "Privilege"
sLogonUserID = "logonuserid" # this is the userid when the user logged in, it won't change even if another user is impersonated
