# -*- coding: utf-8 -*-

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from myapps.s03.views._utils import *
from myapps.s03.views.cache import *

class GlobalView(ExileMixin, View):

    showHeader = False
    selectedMenu = ""
    urlExtraParams = ""
    
    def pre_dispatch(self, request, *args, **kwargs):
        
        #---
        
        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
    
        #---
        
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')

        self.userId = request.user.id
        
        #---
        
        query = "SELECT username, privilege, lastlogin, credits, lastplanetid, deletion_date, score, planets, previous_score," + \
                " alliance_id, alliance_rank, leave_alliance_datetime IS NULL AND (alliance_left IS NULL OR alliance_left < now()) AS can_join_alliance," + \
                " credits_bankruptcy, mod_planets, mod_commanders," + \
                " orientation, prestige_points," + \
                " lcid, security_level" + \
                " FROM users" + \
                " WHERE id=" + str(self.userId)
        self.profile = dbRow(query)
        
        if self.profile == None:
            return HttpResponseRedirect("/")
        
        #---
        
        if self.profile["privilege"] == -1: return HttpResponseRedirect("/s03/locked/")
        if self.profile["privilege"] == -2: return HttpResponseRedirect("/s03/holidays/")
        if self.profile["privilege"] == -3: return HttpResponseRedirect("/s03/wait/")
        
        if self.profile["credits_bankruptcy"] <= 0: return HttpResponseRedirect("/s03/game-over/")

        self.allianceId = self.profile["alliance_id"]
        self.allianceRankId = self.profile["alliance_rank"]
        
        #---
    
        self.allianceRights = None
        
        if self.allianceId:
        
            query = "SELECT label, leader, can_invite_player, can_kick_player, can_create_nap, can_break_nap, can_ask_money, can_see_reports, can_accept_money_requests, can_change_tax_rate, can_mail_alliance," + \
                    " can_manage_description, can_manage_announce, can_see_members_info, can_use_alliance_radars, can_order_other_fleets" + \
                    " FROM alliances_ranks" + \
                    " WHERE allianceid=" + str(self.allianceId) + " AND rankid=" + str(self.allianceRankId)
            self.allianceRights = dbRow(query)
        
        #---

        if not self.request.user.is_impersonate:
        
            oConnDoQuery("SELECT sp_log_activity(" + str(self.userId) + "," + dosql(self.request.META.get("REMOTE_ADDR")) + ", 0)")
            oConnDoQuery("UPDATE users SET lastlogin=now() WHERE id=" + str(self.userId))
        
        #---
        
        response = self.manageCurrentPlanet()
        if response: return response

    def manageCurrentPlanet(self):
        
        #---
        
        planetId = int(self.request.GET.get("planet", 0))        
        if planetId != 0 and planetId != self.profile['lastplanetid']:
            planet = dbRow("SELECT galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND id=" + str(planetId) + " and ownerid=" + str(self.userId))
            if planet:
            
                self.currentPlanetId = planetId
                self.currentPlanetGalaxy = planet['galaxy']
                self.currentPlanetSector = planet['sector']
                
                if not self.request.user.is_impersonate:
                    oConnDoQuery("UPDATE users SET lastplanetid=" + str(planetId) + " WHERE id=" + str(self.userId))
                
                return
                
        #---
        
        self.currentPlanetId = self.profile['lastplanetid']
        if self.currentPlanetId != None and self.currentPlanetId != "":
            planet = dbRow("SELECT galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND id=" + str(self.currentPlanetId) + " AND ownerid=" + str(self.userId))
            if planet:
            
                self.currentPlanetGalaxy = planet['galaxy']
                self.currentPlanetSector =  planet['sector']
                
                return

        #---
        
        planet = dbRow("SELECT id, galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=" + str(self.userId) + " LIMIT 1")    
        if planet == None:
            return HttpResponseRedirect("/s03/game-over/")
    
        self.currentPlanetId = planet['id']
        self.currentPlanetGalaxy = planet['galaxy']
        self.currentPlanetSector = planet['sector']
    
        if not self.request.user.is_impersonate:
            oConnDoQuery("UPDATE users SET lastplanetid=" + str(self.currentPlanetId) + " WHERE id=" + str(self.userId))

    def display(self, tpl):
        
        tpl.setValue("profile_credits", self.profile["credits"])
        tpl.setValue("profile_prestige_points", self.profile["prestige_points"])
        
        #---
        
        if self.showHeader == True:
            
            query = "SELECT ore, ore_production, ore_capacity, mod_production_ore," + \
                    " hydrocarbon, hydrocarbon_production, hydrocarbon_capacity, mod_production_hydrocarbon," + \
                    " energy, energy_consumption, energy_production, energy_capacity," + \
                    " workers, workers_busy, workers_capacity, workers_for_maintenance," + \
                    " scientists, scientists_capacity," + \
                    " soldiers, soldiers_capacity," + \
                    " floor_occupied, floor," + \
                    " space_occupied, space" + \
                    " FROM vw_planets WHERE id=" + str(self.currentPlanetId)
            currentPlanet = dbRow(query)
            tpl.setValue("currentPlanet", currentPlanet)
        
            currentPlanet['ore_level'] = self.getPercent(currentPlanet['ore'], currentPlanet['ore_capacity'], 10)
            if currentPlanet['mod_production_ore'] < 0 or currentPlanet['workers'] < currentPlanet['workers_for_maintenance']: tpl.Parse("medium_ore_production")
            
            currentPlanet['hydrocarbon_level'] = self.getPercent(currentPlanet['hydrocarbon'], currentPlanet['hydrocarbon_capacity'], 10)
            if currentPlanet['mod_production_hydrocarbon'] < 0 or currentPlanet['workers'] < currentPlanet['workers_for_maintenance']: tpl.Parse("medium_hydrocarbon_production")
            
            currentPlanet['workers_idle'] = currentPlanet['workers'] - currentPlanet['workers_busy']  
            if currentPlanet['workers'] < currentPlanet['workers_for_maintenance']: tpl.Parse("workers_low")
        
            if currentPlanet['soldiers'] * 250 < currentPlanet['workers'] + currentPlanet['scientists']: tpl.Parse("soldiers_low")
            
            currentPlanet["energy_production"] -= currentPlanet["energy_consumption"]
            
            #---
            
            if self.urlExtraParams != "": tpl.setValue("url", "?" + self.urlExtraParams + "&planet=")
            else: tpl.setValue("url", "?planet=")

            #---
            
            query = "SELECT id, name, galaxy, sector, planet" + \
                    " FROM nav_planet" + \
                    " WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=" + str(self.userId) + \
                    " ORDER BY id"
            planets = dbRows(query)
            tpl.setValue("planets", planets)
        
            #---
            
            query = "SELECT label" + \
                    " FROM planet_buildings INNER JOIN db_buildings ON (db_buildings.id=buildingid AND db_buildings.is_planet_element)" + \
                    " WHERE planetid=" + str(self.currentPlanetId) + \
                    " ORDER BY upper(db_buildings.label)"
            specials = dbRows(query)
            tpl.setValue("specials", specials)
            
            #---
            
            tpl.Parse("header")
        
        #---
        
        query = "SELECT (SELECT int4(COUNT(*)) FROM messages WHERE ownerid=" + str(self.userId) + " AND read_date is NULL)," + \
                "(SELECT int4(COUNT(*)) FROM reports WHERE ownerid=" + str(self.userId) + " AND read_date is NULL AND datetime <= now());"
        oRs = oConnExecute(query)
        
        tpl.setValue("new_mail", oRs[0])
        tpl.setValue("new_report", oRs[1])
        
        #---
        
        if self.allianceRights:
        
            if self.allianceRights["leader"] or self.allianceRights["can_manage_description"] or self.allianceRights["can_manage_announce"]: tpl.Parse("show_management")
            if self.allianceRights["leader"]: tpl.Parse("show_ranks")
            if self.allianceRights["leader"] or self.allianceRights["can_see_reports"]: tpl.Parse("show_reports")
            if self.allianceRights["leader"] or self.allianceRights["can_see_members_info"]: tpl.Parse("show_members")
        
        #---
        
        tpl.setValue("cur_planetid", self.currentPlanetId)
        tpl.setValue("cur_g", self.currentPlanetGalaxy)
        tpl.setValue("cur_s", self.currentPlanetSector)
        tpl.setValue("cur_p", ((self.currentPlanetId - 1) % 25) + 1)
        
        #---
        
        tpl.setValue("selectedmenu", self.selectedMenu.replace(".", "_"))
        
        #---
        
        if self.profile["deletion_date"]:
        
            tpl.setValue("delete_datetime", self.profile["deletion_date"])
            tpl.Parse("deleting")
        
        #---
        
        if self.profile["credits"] < 0:
        
            tpl.setValue("bankruptcy_hours", self.profile["credits_bankruptcy"])
            tpl.Parse("creditswarning")
        
        #---
        
        if self.request.user.is_impersonate:
        
            tpl.setValue("username", self.profile["username"])
            tpl.Parse("impersonating")
        
        #---
        
        return render(self.request, tpl.template, tpl.data)
        
    def hasRight(self, right):
    
        if self.allianceRights == None: return True
        else: return self.allianceRights["leader"] or self.allianceRights[right]
    
    def getPlanetName(self, relation, radar_strength, ownerName, planetName):
    
        if relation == rSelf: return planetName if planetName else ""
        elif relation == rAlliance: return ownerName if ownerName else ""
        elif relation == rFriend: return ownerName if ownerName else ""
        else:
            if radar_strength > 0: return ownerName if ownerName else ""
            else: return ""

    def planetImg(self, id, floor):
    
        img = 1 + (floor + id) % 21
        if img < 10: img = "0" + str(img)
        return str(img)

    def getPercent(self, current, max, slice):
    
        if (current >= max) or (max == 0): return 100
        else: return slice * int(100 * current / max / slice)
