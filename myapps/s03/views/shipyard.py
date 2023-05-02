# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):
    
    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        #---
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
    
        #---
        
        action = request.GET.get("a", "").lower()
    
        if action == "build":
        
            #---
            
            rows = dbRows("SELECT id FROM db_ships")
            for row in rows:
            
                quantity = ToInt(request.POST.get("s" + str(row['id'])), 0)
                if quantity > 0:
                    dbQuery("SELECT sp_start_ship(" + str(self.currentPlanetId) + "," + str(row['id']) + "," + str(quantity) + ", false)")
        
        elif action == "recycle":
        
            #---
            
            rows = dbRows("SELECT id FROM db_ships")
            for row in rows:
            
                quantity = ToInt(request.POST.get("s" + str(row['id'])), 0)
                if quantity > 0:
                    dbQuery("SELECT sp_start_ship_recycling(" + str(self.currentPlanetId) + "," + str(row['id']) + "," + str(quantity) + ")")
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    def get(self, request, *args, **kwargs):
    
        #---
        
        action = request.GET.get("a", "").lower()
        
        if action == "cancel":
        
            queueId = ToInt(request.GET.get("q"), 0)
            if queueId != 0:            
                dbQuery("SELECT sp_cancel_ship(" + str(self.currentPlanetId) + ", " + str(queueId) + ")")                
            
        #---
        
        self.selectedMenu = "planet"
        
        self.headerUrl = '/s03/shipyard/'
        self.showHeader = True

        #---
        
        query = "SELECT ore_capacity, hydrocarbon_capacity, energy_capacity, workers_capacity" + \
                " FROM vw_planets WHERE id=" + str(self.currentPlanetId)
        planet = dbRow(query)
        
        #---
        
        if request.GET.get("recycle", "") != "":
            
            #---
            
            content = getTemplate(self.request, "s03/shipyard-recycle")
            
            #---
            
            query = "SELECT v.id, v.category, v.label, v.description, int4(v.cost_ore * const_recycle_ore(planet_ownerid)) AS cost_ore, int4(v.cost_hydrocarbon * const_recycle_hydrocarbon(planet_ownerid)) AS cost_hydrocarbon, v.cost_credits, v.workers, v.crew, v.capacity," + \
                    " int4(const_ship_recycling_multiplier() * v.construction_time) as construction_time, v.hull, v.shield, v.weapon_power, v.weapon_ammo, v.weapon_tracking_speed, v.weapon_turrets, v.signature, v.speed," + \
                    " v.handling, v.buildingid, v.recycler_output, v.droppods, v.long_distance_capacity, v.quantity, true, true," + \
                    " NULL, 0, COALESCE(v.new_shipid, v.id) AS shipid" + \
                    " FROM vw_ships AS v" + \
                    "   INNER JOIN db_ships AS db ON db.id = v.id" + \
                    "   LEFT JOIN db_ships AS r ON r.id = v.required_shipid" + \
                    " WHERE quantity > 0 AND planetid=" + str(self.currentPlanetId)
            rows = dbRows(query)
            
            categories = []
            content.setValue("categories", categories)
            
            lastCategory = -1        
            for row in rows:
                
                catId = row['category']
                if catId != lastCategory:
                    lastCategory = catId
                
                    category = { 'id':catId, 'ships':[] }
                    categories.append(category)

                category['ships'].append(row)
            
        else:
            
            #---
            
            content = getTemplate(self.request, "s03/shipyard")

            #---
            
            query = "SELECT v.id, v.category, v.label, v.cost_ore, v.cost_hydrocarbon, v.cost_energy, v.workers, v.crew, v.capacity, v.description," + \
                    " v.construction_time, v.hull, v.shield, v.weapon_power, v.weapon_ammo, v.weapon_tracking_speed, v.weapon_turrets, v.signature, v.speed," + \
                    " v.handling, v.buildingid, v.recycler_output, v.droppods, v.long_distance_capacity, v.quantity, v.buildings_requirements_met, v.research_requirements_met," + \
                    " v.required_shipid, v.required_ship_count, COALESCE(v.new_shipid, v.id) AS shipid, v.cost_prestige, v.upkeep, v.required_vortex_strength, v.mod_leadership, r.label AS r_label" + \
                    " FROM vw_ships AS v" + \
                    "   INNER JOIN db_ships AS db ON db.id = v.id" + \
                    "   LEFT JOIN db_ships AS r ON r.id = v.required_shipid" + \
                    " WHERE planetid=" + str(self.currentPlanetId) + \
                    " ORDER BY category, id"
            rows = dbRows(query)
            
            categories = []
            content.setValue("categories", categories)
            
            lastCategory = -1        
            for row in rows:
                if (row["quantity"] > 0) or row["research_requirements_met"]:
                
                    catId = row['category']
                    if catId != lastCategory:
                        lastCategory = catId
                    
                        category = { 'id':catId, 'ships':[] }
                        categories.append(category)

                    category['ships'].append(row)
                    
                    row['notenoughresources'] = False
                    
                    if row["cost_prestige"] > self.profile["prestige_points"]:
                        row["required_pp_not_enough"] = True
                        row['notenoughresources'] = True
                    
                    if row["cost_ore"] > planet['ore_capacity']:
                        row["not_enough_ore"] = True
                        row['notenoughresources'] = True
                    
                    if row["cost_hydrocarbon"] > planet['hydrocarbon_capacity']:
                        row["not_enough_hydrocarbon"] = True
                        row['notenoughresources'] = True
                    
                    if row["cost_energy"] > planet['energy_capacity']:
                        row["not_enough_energy"] = True
                        row['notenoughresources'] = True
                    
                    if row["crew"] > planet['workers_capacity']:
                        row["not_enough_crew"] = True
                        row['notenoughresources'] = True
            
        #---
        
        query = "SELECT s.id, shipid, remaining_time, quantity, end_time, recycle, s.required_shipid, int4(s.cost_ore*const_recycle_ore(ownerid)) AS r_cost_ore, int4(s.cost_hydrocarbon*const_recycle_hydrocarbon(ownerid)) AS r_cost_hydrocarbon, s.cost_ore, s.cost_hydrocarbon, s.cost_energy, s.crew," + \
                " db_ships.label, r.label AS r_label" + \
                " FROM vw_ships_under_construction AS s" + \
                "   INNER JOIN db_ships ON db_ships.id = shipid" + \
                "   LEFT JOIN db_ships AS r ON r.id = s.required_shipid" + \
                " WHERE planetid=" + str(self.currentPlanetId) + \
                " ORDER BY start_time, shipid"
        rows = dbRows(query)

        queues = []
        content.setValue("queues", queues)
        
        underconstructions = []
        content.setValue("underconstructions", underconstructions)
        
        for row in rows:
        
            if row['end_time']: underconstructions.append(row)
            else: queues.append(row)
        
        #---
        
        return self.display(content)
