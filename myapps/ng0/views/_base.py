# -*- coding: utf-8 -*-

from myapps.ng0.views._utils import *

class BaseView(LoginRequiredMixin, View):
    
    def dispatch(self, request, *args, **kwargs):
    
        #---
        
        if not request.user.is_authenticated: return HttpResponseRedirect('/')
            
        if maintenance: return HttpResponseRedirect('/ng0/home-maintenance/')
        
        dbConnect()
        
        self.userId = request.user.id
        
        #---
        
        if hasattr(self.__class__, 'pre_dispatch'):
        
            response = self.pre_dispatch(request, *args, **kwargs)
            if response: return response
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

class GetView(BaseView):
    
    show_header = False
    
    tab_selected = ''
    menu_selected = ''
    
    template_name = ''
    
    def pre_dispatch(self, request, *args, **kwargs):
    
        #---
        
        query = "SELECT username, privilege, credits, lastplanetid, deletion_date, score, orientation, prestige_points" + \
                " FROM users" + \
                " WHERE id=" + str(self.userId)
        self.profile = dbRow(query)
        
        if self.profile == None: return HttpResponseRedirect("/")
        
        if self.profile["privilege"] == -3: return HttpResponseRedirect("/s03/wait/")
        
        #---

        if not request.user.is_impersonate:
        
            dbQuery("SELECT sp_log_activity(" + str(self.userId) + "," + dosql(request.META.get("REMOTE_ADDR")) + ", 0)")
            dbQuery("UPDATE users SET lastlogin=now() WHERE id=" + str(self.userId))
        
        #---
        
        planetId = int(request.GET.get("planet", 0))        
        if planetId != 0 and planetId != self.profile['lastplanetid']:
            planet = dbRow("SELECT galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND id=" + str(planetId) + " and ownerid=" + str(self.userId))
            if planet:
            
                self.currentPlanetId = planetId
                self.currentPlanetGalaxy = planet['galaxy']
                self.currentPlanetSector = planet['sector']
                
                if not request.user.is_impersonate:
                    dbQuery("UPDATE users SET lastplanetid=" + str(planetId) + " WHERE id=" + str(self.userId))
                
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
    
        if not request.user.is_impersonate:
            dbQuery("UPDATE users SET lastplanetid=" + str(self.currentPlanetId) + " WHERE id=" + str(self.userId))
            
    def get(self, request, *args, **kwargs):
    
        #---
        
        return self.render(request)
    
    def render(self, request):
    
        #---
        
        self.display(request)
        
        #---
    
        tpl.setValue("profile_credits", self.profile["credits"])
        tpl.setValue("profile_prestige_points", self.profile["prestige_points"])
        tpl.setValue("profile_alliance_id", self.allianceId)
        
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
            
            if self.urlExtraParams != "": tpl.setValue("url", self.headerUrl + "?" + self.urlExtraParams + "&planet=")
            else: tpl.setValue("url", self.headerUrl + "?planet=")

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
        
        query = "SELECT (SELECT int4(COUNT(*)) FROM messages WHERE ownerid=" + str(self.userId) + " AND read_date is NULL) AS new_mail," + \
                "(SELECT int4(COUNT(*)) FROM reports WHERE ownerid=" + str(self.userId) + " AND read_date is NULL AND datetime <= now()) AS new_report"
        row = dbRow(query)
        
        tpl.setValue("new_mail", row['new_mail'])
        tpl.setValue("new_report", row['new_report'])
        
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
        
        if request.user.is_impersonate:
        
            tpl.setValue("username", self.profile["username"])
            tpl.Parse("impersonating")
        
        #---
        
        return render(request, tpl.template, tpl.data)

class GetPostView(GetView):
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action').strip().lower()

        response = self.process(request, tpl, action)
        if response: return response
        
        #---
        
        return self.render(request)
