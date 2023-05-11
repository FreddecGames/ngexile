# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    ################################################################################

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        #---
        
        self.commanderId = ToInt(request.GET.get("id"), 0)
        if self.commanderId == 0:
            return HttpResponseRedirect("/s03/")
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

    ################################################################################
    
    def post(self, request, *args, **kwargs):
                
        #---

        action = request.POST.get('action')
        
        #---

        if action == 'save':
        
            ore = max(0, ToInt(request.POST.get("ore"), 0))
            hydrocarbon = max(0, ToInt(request.POST.get("hydrocarbon"), 0))
            energy = max(0, ToInt(request.POST.get("energy"), 0))
            workers = max(0, ToInt(request.POST.get("workers"), 0))

            fleetspeed = max(0, ToInt(request.POST.get("fleet_speed"), 0))
            fleetshield = max(0, ToInt(request.POST.get("fleet_shield"), 0))
            fleethandling = max(0, ToInt(request.POST.get("fleet_handling"), 0))
            fleettargeting = max(0, ToInt(request.POST.get("fleet_targeting"), 0))
            fleetdamages = max(0, ToInt(request.POST.get("fleet_damages"), 0))
            fleetsignature = max(0, ToInt(request.POST.get("fleet_signature"), 0))

            build = max(0, ToInt(request.POST.get("buildindspeed"), 0))
            ship = max(0, ToInt(request.POST.get("shipconstructionspeed"), 0))

            total = ore + hydrocarbon + energy + workers + fleetspeed + fleetshield + fleethandling + fleettargeting + fleetdamages + fleetsignature + build + ship
            
            query = "UPDATE commanders SET" + \
                    "    mod_production_ore=mod_production_ore + 0.01*" + str(ore) + \
                    "    ,mod_production_hydrocarbon=mod_production_hydrocarbon + 0.01*" + str(hydrocarbon) + \
                    "    ,mod_production_energy=mod_production_energy + 0.1*" + str(energy) + \
                    "    ,mod_production_workers=mod_production_workers + 0.1*" + str(workers) + \
                    "    ,mod_fleet_speed=mod_fleet_speed + 0.02*" + str(fleetspeed) + \
                    "    ,mod_fleet_shield=mod_fleet_shield + 0.02*" + str(fleetshield) + \
                    "    ,mod_fleet_handling=mod_fleet_handling + 0.05*" + str(fleethandling) + \
                    "    ,mod_fleet_tracking_speed=mod_fleet_tracking_speed + 0.05*" + str(fleettargeting) + \
                    "    ,mod_fleet_damage=mod_fleet_damage + 0.02*" + str(fleetdamages) + \
                    "    ,mod_fleet_signature=mod_fleet_signature + 0.02*" + str(fleetsignature) + \
                    "    ,mod_construction_speed_buildings=mod_construction_speed_buildings + 0.05*" + str(build) + \
                    "    ,mod_construction_speed_ships=mod_construction_speed_ships + 0.05*" + str(ship) + \
                    "    ,points=points-" + str(total) + \
                    " WHERE ownerid=" + str(self.userId) + " AND id=" + str(self.commanderId) + " AND points >= " + str(total)
            dbQuery(query)

            query = "SELECT sp_commanders_update_salary(" + str(self.userId) + ", " + str(self.commanderId) + ")"
            dbQuery(query)

            query = "SELECT sp_update_fleet_bonus(id) FROM fleets WHERE commanderid=" + str(self.commanderId)
            dbQuery(query)

            query = "SELECT sp_update_planet(id) FROM nav_planet WHERE commanderid=" + str(self.commanderId)
            dbQuery(query)

            return HttpResponseRedirect("/s03/commander-list/")
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---
        
        tpl = getTemplate(request, "s03/commanders")

        self.selectedMenu = "commanders"

        #---
        
        query = "SELECT id, mod_production_ore, mod_production_hydrocarbon, mod_production_energy," + \
                " mod_production_workers, mod_fleet_speed, mod_fleet_shield, mod_fleet_handling," + \
                " mod_fleet_tracking_speed, mod_fleet_damage, mod_fleet_signature," + \
                " mod_construction_speed_buildings, mod_construction_speed_ships," + \
                " points, name" + \
                " FROM commanders WHERE points > 0 AND id=" + str(self.commanderId) + " AND ownerid=" + str(self.userId)
        commander = dbRow(query)
        tpl.setValue('commander', commander)
        
        commander['mod_production_ore'] = str(commander['mod_production_ore']).replace(",", ".")
        commander["mod_production_hydrocarbon"] = str(commander['mod_production_hydrocarbon']).replace(",", ".")
        commander["mod_production_energy"] = str(commander['mod_production_energy']).replace(",", ".")
        commander["mod_production_workers"] = str(commander['mod_production_workers']).replace(",", ".")

        commander["mod_fleet_speed"] = str(commander['mod_fleet_speed']).replace(",", ".")
        commander["mod_fleet_shield"] = str(commander['mod_fleet_shield']).replace(",", ".")
        commander["mod_fleet_handling"] = str(commander['mod_fleet_handling']).replace(",", ".")
        commander["mod_fleet_tracking_speed"] = str(commander['mod_fleet_tracking_speed']).replace(",", ".")
        commander["mod_fleet_damage"] = str(commander['mod_fleet_damage']).replace(",", ".")
        commander["mod_fleet_signature"] = str(commander['mod_fleet_signature']).replace(",", ".")

        commander["mod_construction_speed_buildings"] = str(commander['mod_construction_speed_buildings']).replace(",", ".")
        commander["mod_construction_speed_ships"] = str(commander['mod_construction_speed_ships']).replace(",", ".")
        
        #---
        
        return self.display(tpl, request)
