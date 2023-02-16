# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from myapps.s03.views._utils import *

from myapps.s03.views.cache import *

class GlobalView(ExileMixin, View):

    CurrentPlanet = None
    CurrentGalaxyId = None
    CurrentSectorId = None
    showHeader = False
    url_extra_params = ""
    displayAlliancePlanetName = True
    selectedMenu = ""
    
    def pre_dispatch(self, request, *args, **kwargs):
        
        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
    
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')

        self.userId = request.user.id
        
        response = self.CheckSessionValidity()
        if response: return response
        
        # Check for the planet querystring parameter and if the current planet belongs to the player
        response = self.CheckCurrentPlanetValidity()
        if response: return response
        
    def hasRight(self, right):
        if self.oAllianceRights == None:
            return True
        else:
            return self.oAllianceRights["leader"] or self.oAllianceRights[right]
    
    def getPlanetName(self, relation, radar_strength, ownerName, planetName):
        if relation == rSelf:
            return planetName if planetName else ""
        elif relation == rAlliance:
            if self.displayAlliancePlanetName:
                return planetName if planetName else ""
            else:
                return ownerName if ownerName else ""
        elif relation == rFriend:
            return ownerName if ownerName else ""
        else:
            if radar_strength > 0:
                return ownerName if ownerName else ""
            else:
                return ""

    def IsImpersonating(self):
        return self.request.user.is_impersonate

    # return image of a planet according to its it and its floor
    def planetimg(self,id,floor):
        img = 1+(floor + id) % 21
        if img < 10: img = "0" + str(img)
        return str(img)

    # return the percentage of the current value compared to max value
    def getpercent(self, current, max, slice):
        if (current >= max) or (max == 0):
            return 100
        else:
            return slice*int(100 * current / max / slice)

    #
    # Parse the header, list the planets owned by the player and show the resources of the current planet
    #
    def fillHeader(self, tpl):

        query = "SELECT ore, ore_production, ore_capacity," + \
                " hydrocarbon, hydrocarbon_production, hydrocarbon_capacity," + \
                " workers, workers_busy, workers_capacity," + \
                " energy_consumption, energy_production," + \
                " floor_occupied, floor," + \
                " space_occupied, space, workers_for_maintenance," + \
                " mod_production_ore, mod_production_hydrocarbon, energy, energy_capacity, soldiers, soldiers_capacity, scientists, scientists_capacity" + \
                " FROM vw_planets WHERE id=" + str(self.CurrentPlanet)
        oRs = oConnExecute(query)
    
        tpl.setValue("ore", oRs[0])
        tpl.setValue("ore_production", oRs[1])
        tpl.setValue("ore_capacity", oRs[2])
    
        # compute ore level : ore / capacity
        ore_level = self.getpercent(oRs[0], oRs[2], 10)
    
        if ore_level >= 90:
            tpl.Parse("high_ore")
        elif ore_level >= 70:
            tpl.Parse("medium_ore")
        else:
            tpl.Parse("normal_ore")
    
        tpl.setValue("hydrocarbon", oRs[3])
        tpl.setValue("hydrocarbon_production", oRs[4])
        tpl.setValue("hydrocarbon_capacity", oRs[5])
    
        hydrocarbon_level = self.getpercent(oRs[3], oRs[5], 10)
    
        if hydrocarbon_level >= 90:
            tpl.Parse("high_hydrocarbon")
        elif hydrocarbon_level >= 70:
            tpl.Parse("medium_hydrocarbon")
        else:
            tpl.Parse("normal_hydrocarbon")
    
        tpl.setValue("workers", oRs[6])
        tpl.setValue("workers_capacity", oRs[8])
        tpl.setValue("workers_idle", oRs[6] - oRs[7])
    
        if oRs[6] < oRs[15]: tpl.Parse("workers_low")
    
        tpl.setValue("soldiers", oRs[20])
        tpl.setValue("soldiers_capacity", oRs[21])
    
        if oRs[20]*250 < oRs[6]+oRs[22]: tpl.Parse("soldiers_low")
    
        tpl.setValue("scientists", oRs[22])
        tpl.setValue("scientists_capacity", oRs[23])
    
        tpl.setValue("energy_consumption", oRs[9])
        tpl.setValue("energy_totalproduction", oRs[10])
        tpl.setValue("energy_production", oRs[10]-oRs[9])
    
        tpl.setValue("energy", oRs[18])
        tpl.setValue("energy_capacity", oRs[19])
    
        if oRs[9] > oRs[10]: tpl.Parse("energy_low")
    
        if oRs[9] > oRs[10]: tpl.Parse("energy_production_minus")
        else: tpl.Parse("energy_production_normal")
    
        tpl.setValue("floor_occupied", oRs[11])
        tpl.setValue("floor", oRs[12])
    
        tpl.setValue("space_occupied", oRs[13])
        tpl.setValue("space", oRs[14])
    
        # ore/hydro production colors
        if oRs[16] >= 0 and oRs[6] >= oRs[15]:
            tpl.Parse("normal_ore_production")
        else:
            tpl.Parse("medium_ore_production")

        if oRs[17] >= 0 and oRs[6] >= oRs[15]:
            tpl.Parse("normal_hydrocarbon_production")
        else:
            tpl.Parse("medium_hydrocarbon_production")

        #
        # Fill the planet list
        #
        if self.url_extra_params != "":
            tpl.setValue("url", "?" + self.url_extra_params + "&planet=")
        else:
            tpl.setValue("url", "?planet=")

        # cache the list of planets as they are not supposed to change unless a colonization occurs
        # in case of colonization, let the colonize script reset the session value
        # retrieve planet list
        query = "SELECT id, name, galaxy, sector, planet" + \
                " FROM nav_planet" + \
                " WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=" + str(self.userId) + \
                " ORDER BY id"
        oRs = oConnExecuteAll(query)

        if oRs == None:
            planetListCount = -1
        else:
            planetListArray = oRs
            planetListCount = len(oRs)

        planets = []
        for item in planetListArray:
            id = item[0]
    
            planet = {}
            planets.append(planet)
            
            planet["id"] = id
            planet["name"] = item[1]
            planet["g"] = item[2]
            planet["s"] = item[3]
            planet["p"] = item[4]
    
            if id == self.CurrentPlanet: planet["selected"] = True
    
        tpl.setValue("planets", planets)
    
        query = "SELECT buildingid" +\
                " FROM planet_buildings INNER JOIN db_buildings ON (db_buildings.id=buildingid AND db_buildings.is_planet_element)" +\
                " WHERE planetid="+str(self.CurrentPlanet)+\
                " ORDER BY upper(db_buildings.label)"
        oRs = oConnExecuteAll(query)
    
        i = 0
        if oRs:
            for item in oRs:

                if i % 3 == 0:
                    tpl.setValue("special1", getBuildingLabel(item[0]))
                elif i % 3 == 1:
                    tpl.setValue("special2", getBuildingLabel(item[0]))
                else:
                    tpl.setValue("special3", getBuildingLabel(item[0]))
                    tpl.Parse("special")
        
                i = i + 1
    
        if i % 3 != 0: tpl.Parse("special")
    
    #
    # Parse the menu
    #
    def fillMenu(self, tpl_layout):
        # Initialize the menu template

        tpl = tpl_layout
    
        # retrieve number of new messages & reports
        query = "SELECT (SELECT int4(COUNT(*)) FROM messages WHERE ownerid=" + str(self.userId) + " AND read_date is NULL)," + \
                "(SELECT int4(COUNT(*)) FROM reports WHERE ownerid=" + str(self.userId) + " AND read_date is NULL AND datetime <= now());"
        oRs = oConnExecute(query)
        
        if oRs[0] > 0:
            tpl.setValue("new_mail", oRs[0])

        if oRs[1] > 0:
            tpl.setValue("new_report", oRs[1])

        if self.oAllianceRights:
            if self.oAllianceRights["leader"] or self.oAllianceRights["can_manage_description"] or self.oAllianceRights["can_manage_announce"]: tpl.Parse("show_management")
            if self.oAllianceRights["leader"] or self.oAllianceRights["can_see_reports"]: tpl.Parse("show_reports")
            if self.oAllianceRights["leader"] or self.oAllianceRights["can_see_members_info"]: tpl.Parse("show_members")
    
        tpl.setValue("cur_planetid", self.CurrentPlanet)
    
        tpl.setValue("cur_g", self.CurrentGalaxyId)
        tpl.setValue("cur_s", self.CurrentSectorId)
        tpl.setValue("cur_p", ((self.CurrentPlanet-1) % 25) + 1)
    
        tpl.setValue("selectedmenu", self.selectedMenu.replace(".","_"))
    
        if self.selectedMenu != "":
            blockname = self.selectedMenu + "_selected"
    
            while blockname != "":
                tpl.Parse(blockname)
    
                i = blockname.rfind(".")
                if i > 0: i = i - 1
                blockname = blockname[:i]

        # Assign the menu
        tpl_layout.setValue("menu", True)

    def display(self, tpl):
        
        tpl.setValue("profile_credits", self.oPlayerInfo["credits"])
        tpl.setValue("profile_prestige_points", self.oPlayerInfo["prestige_points"])

        if self.showHeader == True:
            self.fillHeader(tpl)
            tpl.Parse("header")

        self.fillMenu(tpl)

        if self.oPlayerInfo["deletion_date"]:
            tpl.setValue("delete_datetime", self.oPlayerInfo["deletion_date"])
            tpl.Parse("deleting")

        if self.oPlayerInfo["credits"] < 0:
            tpl.setValue("bankruptcy_hours", self.oPlayerInfo["credits_bankruptcy"])
            tpl.Parse("creditswarning")

        if self.IsImpersonating():
            tpl.setValue("username", self.oPlayerInfo["username"])
            tpl.Parse("impersonating")

        return render(self.request, tpl.template, tpl.data)

    #
    # Check that our user is valid, otherwise redirect user to home page
    #
    def CheckSessionValidity(self):
    
        # check that this session is still used
        # if a user tries to login multiple times, the first sessions are abandonned

        query = "SELECT username, privilege, lastlogin, credits, lastplanetid, deletion_date, score, planets, previous_score," +\
                "alliance_id, alliance_rank, leave_alliance_datetime IS NULL AND (alliance_left IS NULL OR alliance_left < now()) AS can_join_alliance," +\
                "credits_bankruptcy, mod_planets, mod_commanders," +\
                "ban_datetime, ban_expire, ban_reason, ban_reason_public, orientation, (paid_until IS NOT NULL AND paid_until > now()) AS paid," +\
                " timers_enabled, display_alliance_planet_name, prestige_points, (inframe IS NOT NULL AND inframe) AS inframe, COALESCE(skin, 's_default') AS skin," +\
                "lcid, security_level" +\
                " FROM users" +\
                " WHERE id=" + str(self.userId)
        self.oPlayerInfo = dbRow(query)
        
        # check account still exists or that the player didn't connect with another account meanwhile
        if self.oPlayerInfo == None:
            return HttpResponseRedirect("/") # Redirect to home page
    
        self.displayAlliancePlanetName = self.oPlayerInfo["display_alliance_planet_name"]
        
        if self.oPlayerInfo["privilege"] == -1: return HttpResponseRedirect("/s03/locked/")
        if self.oPlayerInfo["privilege"] == -2: return HttpResponseRedirect("/s03/holidays/")
        if self.oPlayerInfo["privilege"] == -3: return HttpResponseRedirect("/s03/wait/")
        
        if self.oPlayerInfo["credits_bankruptcy"] <= 0: return HttpResponseRedirect("/s03/game-over/")

        self.AllianceId = self.oPlayerInfo["alliance_id"]
        self.AllianceRank = self.oPlayerInfo["alliance_rank"]
        self.oAllianceRights = None
    
        if self.AllianceId:
            query = "SELECT label, leader, can_invite_player, can_kick_player, can_create_nap, can_break_nap, can_ask_money, can_see_reports, can_accept_money_requests, can_change_tax_rate, can_mail_alliance," +\
                    " can_manage_description, can_manage_announce, can_see_members_info, can_use_alliance_radars, can_order_other_fleets" +\
                    " FROM alliances_ranks" +\
                    " WHERE allianceid=" + str(self.AllianceId) + " AND rankid=" + str(self.AllianceRank)
            self.oAllianceRights = dbRow(query)
    
            if self.oAllianceRights == None:
                self.oAllianceRights = None
                self.AllianceId = None

        # log activity
        if not self.IsImpersonating():
            oConnExecute("SELECT sp_log_activity(" + str(self.userId) + "," + dosql(self.request.META.get("REMOTE_ADDR")) + ", 0)")
            oConnDoQuery("UPDATE users SET lastlogin=now() WHERE id=" + str(self.userId))

    # set the new current planet, if the planet doesn't belong to the player then go back to the session planet
    def SetCurrentPlanet(self, planetid):
    
        #
        # Check if a parameter is given and if different than the current planet
        # In that case, try to set it as the new planet : check that this planet belongs to the player
        #
        if (planetid != "") and (planetid != self.CurrentPlanet):
            # check that the new planet belongs to the player
            oRs = oConnExecute("SELECT galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND id=" + str(planetid) + " and ownerid=" + str(self.userId))
            if oRs:
                self.CurrentPlanet = planetid
                self.CurrentGalaxyId = oRs[0]
                self.CurrentSectorId = oRs[1]
                self.request.session[sPlanet] = planetid
    
                # save the last planetid
                if not self.request.user.is_impersonate:
                    oConnDoQuery("UPDATE users SET lastplanetid=" + str(planetid) + " WHERE id=" + str(self.userId))
    
                return
    
        # 
        # retrieve current planet from session
        #
        self.CurrentPlanet = self.request.session.get(sPlanet, "")
    
        if self.CurrentPlanet != None and self.CurrentPlanet != "":
            # check if the planet still belongs to the player
            oRs = oConnExecute("SELECT galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND id=" + str(self.CurrentPlanet) + " AND ownerid=" + str(self.userId))
            if oRs:
                # the planet still belongs to the player, exit
                self.CurrentGalaxyId = oRs[0]
                self.CurrentSectorId = oRs[1]
                return
    
        # there is no active planet, select the first planet available
        oRs = oConnExecute("SELECT id, galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=" + str(self.userId) + " LIMIT 1")
    
        # if player owns no planets then the game is over
        if oRs == None:
            return HttpResponseRedirect("/s03/game-over/")
    
        # assign planet id
        self.CurrentPlanet = oRs[0]
        self.CurrentGalaxyId = oRs[1]
        self.CurrentSectorId = oRs[2]
        self.request.session[sPlanet] = self.CurrentPlanet
    
        # save the last planetid
        if not self.request.user.is_impersonate:
            oConnDoQuery("UPDATE users SET lastplanetid=" + str(self.CurrentPlanet) + " WHERE id=" + str(self.userId))
    
        # a player may wish to destroy a building on a planet that belonged to him
        # if the planet doesn't belong to him anymore, the action may be performed on another planet
        # so we redirect the user to the overview to prevent executing an order on another planet
        return HttpResponseRedirect("/s03/overview/")
    
    #
    # check if a planet is given in the querystring and that it belongs to the player
    #
    def CheckCurrentPlanetValidity(self):
    
        # retrieve planet parameter if any
        id = ToInt(self.request.GET.get("planet"), "")
    
        return self.SetCurrentPlanet(id)
