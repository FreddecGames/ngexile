from .utils import *

from myapps.s03.battle import *

class GlobalView(BaseMixin, View):

    CurrentPlanet = None
    CurrentGalaxyId = None
    CurrentSectorId = None
    
    showHeader = False
    
    def pre_dispatch(self, request, *args, **kwargs):
        
        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        if not request.session.get(sUser):
            return HttpResponseRedirect("/s03/")
        
        self.UserId = self.request.session.get(sUser)

        query = "SELECT username, privilege, credits, lastplanetid, deletion_date, score, planets, previous_score," + \
                " alliance_id, alliance_rank, leave_alliance_datetime IS NULL AND (alliance_left IS NULL OR alliance_left < now()) AS can_join_alliance," + \
                " credits_bankruptcy, mod_planets, mod_commanders," + \
                " orientation, prestige_points" + \
                " FROM users" + \
                " WHERE id=" + str(self.UserId)
        self.oPlayerInfo = oConnRow(query)
        
        if self.oPlayerInfo == None:
            return HttpResponseRedirect("/s03/")

        if self.oPlayerInfo["privilege"] == -1: return HttpResponseRedirect("/s03/home-locked/")
        if self.oPlayerInfo["privilege"] == -2: return HttpResponseRedirect("/s03/home-holidays/")
        if self.oPlayerInfo["privilege"] == -3: return HttpResponseRedirect("/s03/home-wait/")
        
        if self.oPlayerInfo["credits_bankruptcy"] <= 0: return HttpResponseRedirect("/s03/home-gameover/")

        self.AllianceId = self.oPlayerInfo["alliance_id"]
        self.AllianceRank = self.oPlayerInfo["alliance_rank"]
        
        self.oAllianceRights = None    
        if self.AllianceId:
        
            query = "SELECT label, leader, can_invite_player, can_kick_player, can_create_nap, can_break_nap, can_ask_money, can_see_reports, can_accept_money_requests, can_change_tax_rate, can_mail_alliance," + \
                    " can_manage_description, can_manage_announce, can_see_members_info, can_use_alliance_radars, can_order_other_fleets" + \
                    " FROM alliances_ranks" + \
                    " WHERE allianceid=" + str(self.AllianceId) + " AND rankid=" + str(self.AllianceRank)
            self.oAllianceRights = oConnRow(query)
    
            if self.oAllianceRights == None:
                self.oAllianceRights = None
                self.AllianceId = None

        if not self.request.user.is_impersonate:
            oConnExecute("SELECT sp_log_activity(" + str(self.UserId) + "," + dosql(self.request.META.get("REMOTE_ADDR")) + ", 0)")
        
        planetid = ToInt(self.request.GET.get("planet"), 0)
    
        if planetid != "" and planetid != self.CurrentPlanet:

            oRs = oConnExecute("SELECT galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND id=" + str(planetid) + " and ownerid=" + str(self.UserId))
            if oRs:
            
                self.CurrentPlanet = planetid
                self.CurrentGalaxyId = oRs[0]
                self.CurrentSectorId = oRs[1]
    
                if not self.request.user.is_impersonate:
                    oConnDoQuery("UPDATE users SET lastplanetid=" + str(planetid) + " WHERE id=" + str(self.UserId))
    
                return

        self.CurrentPlanet = self.oPlayerInfo["lastplanetid"]        
        if self.CurrentPlanet != None:

            oRs = oConnExecute("SELECT galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND id=" + str(self.CurrentPlanet) + " AND ownerid=" + str(self.UserId))
            if oRs:

                self.CurrentGalaxyId = oRs[0]
                self.CurrentSectorId = oRs[1]
                
                return
    
        oRs = oConnExecute("SELECT id, galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=" + str(self.UserId) + " LIMIT 1")
        if oRs == None:
            return HttpResponseRedirect("/s03/home-gameover/")
    
        self.CurrentPlanet = oRs[0]
        self.CurrentGalaxyId = oRs[1]
        self.CurrentSectorId = oRs[2]
    
        if not self.request.user.is_impersonate:
            oConnDoQuery("UPDATE users SET lastplanetid=" + str(self.CurrentPlanet) + " WHERE id=" + str(self.UserId))

        return HttpResponseRedirect("/s03/empire-view/")

    def Display(self, tpl):
        
        dbRow = oConnRow("SELECT avatar_url, username, credits, prestige_points FROM users WHERE id=" + str(self.UserId))
        tpl.AssignValue("avatar_url", dbRow['avatar_url'])
        tpl.AssignValue("username", dbRow['username'])
        tpl.AssignValue("credits", dbRow['credits'])
        tpl.AssignValue("prestige_points", dbRow['prestige_points'])

        self.FillMenu(tpl)
        
        tpl.AssignValue("deletion_date", self.oPlayerInfo["deletion_date"])

        if self.oPlayerInfo["credits"] < 0:
            tpl.AssignValue("bankruptcy_hours", self.oPlayerInfo["credits_bankruptcy"])

        if self.request.user.is_impersonate:
            tpl.AssignValue("username", self.oPlayerInfo["username"])
            tpl.Parse("impersonating")

        tpl.AssignValue("userid", self.UserId)

        if self.oAllianceRights:
        
            if self.oAllianceRights["leader"] or self.oAllianceRights["can_manage_description"] or self.oAllianceRights["can_manage_announce"]: tpl.Parse("show_management")
            if self.oAllianceRights["leader"] or self.oAllianceRights["can_see_reports"]: tpl.Parse("show_reports")
            if self.oAllianceRights["leader"] or self.oAllianceRights["can_see_members_info"]: tpl.Parse("show_members")
        
        if self.showHeader == True: self.FillHeader(tpl)
        
        '''
        ###########################
        
        query = 'SELECT * FROM db_ships ORDER BY category, id'
        dbRows = oConnRows(query)
        
        for currentShip in dbRows:
            
            if currentShip['id'] < 601:
                
                battle = TBattle()
                
                battle.AddShips(0, 0, currentShip['id'], currentShip['hull'], currentShip['shield'], currentShip['handling'], currentShip['weapon_ammo'], currentShip['weapon_tracking_speed'], currentShip['weapon_turrets'], \
                        {'EM': currentShip['weapon_dmg_em'], 'Explosive': currentShip['weapon_dmg_explosive'], 'Kinetic': currentShip['weapon_dmg_kinetic'], 'Thermal': currentShip['weapon_dmg_thermal']}, \
                        {'Hull': 100.0, 'Shield': 100.0, 'Handling': 100.0, 'Tracking_speed': 100.0, 'Damage': 100.0}, \
                        {'EM': currentShip['resist_em'], 'Explosive': currentShip['resist_explosive'], 'Kinetic': currentShip['resist_kinetic'], 'Thermal': currentShip['resist_thermal']}, \
                        1, True, currentShip['tech'])
                
                for enemyShip in dbRows:
                    if enemyShip['id'] < 601:
                        battle.AddShips(1, 0, enemyShip['id'], enemyShip['hull'], enemyShip['shield'], enemyShip['handling'], enemyShip['weapon_ammo'], enemyShip['weapon_tracking_speed'], enemyShip['weapon_turrets'], \
                                {'EM': enemyShip['weapon_dmg_em'], 'Explosive': enemyShip['weapon_dmg_explosive'], 'Kinetic': enemyShip['weapon_dmg_kinetic'], 'Thermal': enemyShip['weapon_dmg_thermal']}, \
                                {'Hull': 100.0, 'Shield': 100.0, 'Handling': 100.0, 'Tracking_speed': 100.0, 'Damage': 100.0}, \
                                {'EM': enemyShip['resist_em'], 'Explosive': enemyShip['resist_explosive'], 'Kinetic': enemyShip['resist_kinetic'], 'Thermal': enemyShip['resist_thermal']}, \
                                1, True, enemyShip['tech'])
                
                battle.BeginFight()
                
                targetList = battle.FPlayers[0].FGroups[0].FindTargetList()
                
                if battle.FPlayers[0].FGroups[0].FWeapon_turrets > 0:
                    print('#####')
                    dbRow = oConnRow('SELECT label FROM db_ships WHERE id=' + str(battle.FPlayers[0].FGroups[0].FId))
                    print(dbRow['label'])
                    if targetList:
                        for target in targetList:
                            dbRow = oConnRow('SELECT label FROM db_ships WHERE id=' + str(target.FId))                
                            print('\t' + dbRow['label'])
                    print('#####')
        
        ##########################
        '''
        
        return render(self.request, tpl.template, tpl.data)
    
    def FillMenu(self, tpl):
    
        query = "SELECT (SELECT int4(COUNT(*)) FROM messages WHERE ownerid=" + str(self.UserId) + " AND read_date is NULL)," + \
                "(SELECT int4(COUNT(*)) FROM reports WHERE ownerid=" + str(self.UserId) + " AND read_date is NULL AND datetime <= now());"
        oRs = oConnExecute(query)
        
        tpl.AssignValue("new_mail", oRs[0])
        tpl.AssignValue("new_report", oRs[1])
    
        tpl.AssignValue("planetid", self.CurrentPlanet)
    
        tpl.AssignValue("cur_g", self.CurrentGalaxyId)
        tpl.AssignValue("cur_s", self.CurrentSectorId)
        tpl.AssignValue("cur_p", ((self.CurrentPlanet - 1) % 25) + 1)
    
        tpl.AssignValue("selectedmenu", self.selectedMenu)
        
        query = "SELECT int4(count(1)) AS ranking_players, (SELECT int4(count(1)) FROM vw_players WHERE score >= " + str(self.oPlayerInfo["score"]) + ") AS ranking FROM vw_players"
        result = oConnRow(query)
        
        tpl.AssignValue("ranking", result["ranking"])
        tpl.AssignValue("ranking_players", result["ranking_players"])
            
        if self.AllianceId:
        
            query = "SELECT tag, name FROM alliances WHERE id=" + str(self.AllianceId)
            result = oConnRow(query)
            
            tpl.AssignValue("alliance_tag", result["tag"])
            tpl.AssignValue("alliance_name", result["name"])

    def FillHeader(self, tpl):
    
        tpl.Parse("context")
            
        query = "SELECT ore, ore_production, ore_capacity," + \
                "hydrocarbon, hydrocarbon_production, hydrocarbon_capacity," + \
                "workers, workers_busy, workers_capacity," + \
                "energy_consumption, energy_production," + \
                "floor_occupied, floor," + \
                "space_occupied, space, workers_for_maintenance," + \
                "mod_production_ore, mod_production_hydrocarbon, energy, energy_capacity, soldiers, soldiers_capacity, scientists, scientists_capacity" + \
                " FROM vw_planets WHERE id=" + str(self.CurrentPlanet)
        dbRow = oConnRow(query)
        
        dbRow['energy_production'] = dbRow['energy_production'] - dbRow['energy_consumption']
        
        dbRow['ore_level'] = getPercent(dbRow['ore'], dbRow['ore_capacity'], 10)
        dbRow['hydrocarbon_level'] = getPercent(dbRow['hydrocarbon'], dbRow['hydrocarbon_capacity'], 10)
        
        dbRow['workers_idle'] = dbRow['workers'] - dbRow['workers_busy']
        
        if dbRow['soldiers'] * 250 < dbRow['workers'] + dbRow['scientists']: dbRow['soldiers_low'] = True

        if dbRow['mod_production_ore'] < 0 or dbRow['workers'] < dbRow['workers_for_maintenance']: dbRow['ore_production_anormal'] = True
        if dbRow['mod_production_hydrocarbon'] < 0 or dbRow['workers'] < dbRow['workers_for_maintenance']: dbRow['hydrocarbon_production_anormal'] = True

        tpl.AssignValue("planet", dbRow)

        tpl.AssignValue("url", "?planet=")

        query = "SELECT id, name, galaxy, sector, planet" + \
                " FROM nav_planet" + \
                " WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=" + str(self.UserId) + \
                " ORDER BY id"
        dbRows = oConnRows(query)

        planets = []    
        tpl.AssignValue("planets", planets)
        
        for dbRow in dbRows:
    
            planet = dbRow
            planets.append(planet)
                
            if dbRow['id'] == self.CurrentPlanet: dbRow["selected"] = True
    
        query = "SELECT buildingid" +\
                " FROM planet_buildings INNER JOIN db_buildings ON (db_buildings.id=buildingid AND db_buildings.is_planet_element)" +\
                " WHERE planetid="+str(self.CurrentPlanet)+\
                " ORDER BY upper(db_buildings.label)"
        oRs = oConnExecuteAll(query)
    
        i = 0
        for item in oRs:
        
            if i % 3 == 0: tpl.AssignValue("special1", getBuildingLabel(item[0]))
            elif i % 3 == 1: tpl.AssignValue("special2", getBuildingLabel(item[0]))
            else: tpl.AssignValue("special3", getBuildingLabel(item[0]))
    
            i = i + 1
