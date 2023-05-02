# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):

        self.selectedMenu = "help"

        content = getTemplate(request, "s03/help")
        
        #---

        cat = request.GET.get("cat", "")
        if cat == "" or cat != "buildings" and cat != "research" and cat != "ships" and cat != "orientations" and cat != "battle" and cat != "tags":
            cat = "general"
            
        content.Parse(cat)

        #---
        
        if cat == "buildings":
        
            query = "SELECT id, category," + \
                    " cost_ore, cost_hydrocarbon, workers, floor, space, production_ore, production_hydrocarbon, energy_production, (workers*maintenance_factor/100.0)::integer AS upkeep_workers, upkeep AS upkeep_credits, energy_consumption AS upkeep_energy," + \
                    " storage_ore, storage_hydrocarbon, storage_energy," + \
                    " label, description" + \
                    " FROM sp_list_available_buildings(" + str(self.userId) + ")" + \
                    " WHERE not is_planet_element"
            results = dbRows(query)

            lastCategory = -1

            categories = []
            content.setValue("categories", categories)
            
            for result in results:
                
                if result['category'] != lastCategory:
                    lastCategory = result['category']
                    
                    category = {'id': result['category'], 'buildings':[]}
                    categories.append(category)

                category['buildings'].append(result)

        #---

        elif cat == "research":
        
            query = "SELECT researchid, category, total_cost," + \
                    " label, description" + \
                    " FROM sp_list_researches(" + str(self.userId) + ") WHERE level > 0 OR (researchable AND planet_elements_requirements_met)" + \
                    " ORDER BY category, researchid"
            results = dbRows(query)

            lastCategory = -1

            categories = []
            content.setValue("categories", categories)
            
            for result in results:
                
                if result['category'] != lastCategory:
                    lastCategory = result['category']
                    
                    category = {'id': result['category'], 'researches':[]}
                    categories.append(category)

                category['researches'].append(result)

        #---

        elif cat == "ships":

            query = "SELECT shipid, required_buildingid, label" + \
                    " FROM db_ships_req_building" + \
                    " INNER JOIN db_buildings ON id=required_buildingid"
            shipReqs = dbRows(query)
            
            query = "SELECT id, category, cost_ore, cost_hydrocarbon, crew," + \
                    " signature, capacity, handling, speed, weapon_turrets, weapon_dmg_em + weapon_dmg_explosive + weapon_dmg_kinetic + weapon_dmg_thermal AS weapon_power, " + \
                    " weapon_tracking_speed, hull, shield, recycler_output, long_distance_capacity, droppods, cost_energy, upkeep, required_vortex_strength, leadership," + \
                    " label, description" + \
                    " FROM sp_list_available_ships(" + str(self.userId) + ") WHERE new_shipid IS NULL"
            results = dbRows(query)

            lastCategory = -1

            categories = []
            content.setValue("categories", categories)
            
            for result in results:
                
                if result['category'] != lastCategory:
                    lastCategory = result['category']
                    
                    category = {'id': result['category'], 'ships':[]}
                    categories.append(category)

                category['ships'].append(result)
                
                result["buildings"] = []
                for req in shipReqs:
                    if req['shipid'] == result["id"]:
                        result["buildings"].append(req['label'])

        #---

        return self.display(content, request)
