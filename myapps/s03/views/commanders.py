# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        commanderId = ToInt(request.POST.get("id"), 0)
        
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
                " WHERE ownerid=" + str(self.userId) + " AND id=" + str(commanderId) + " AND points >= " + str(total)
        dbQuery(query)

        query = "SELECT sp_commanders_update_salary(" + str(self.userId) + ", " + str(commanderId) + ")"
        dbQuery(query)

        query = "SELECT sp_update_fleet_bonus(id) FROM fleets WHERE commanderid=" + str(commanderId)
        dbQuery(query)

        query = "SELECT sp_update_planet(id) FROM nav_planet WHERE commanderid=" + str(commanderId)
        dbQuery(query)

        return HttpResponseRedirect("/s03/commanders/")
        
    def get(self, request, *args, **kwargs):
        
        action = request.GET.get('a', '').lower()
        
        #---
        
        if action == 'rename':        
            commanderId = ToInt(request.GET.get("id"), 0)
            newName = request.GET.get("name")            
            query = "SELECT sp_commanders_rename(" + str(self.userId) + "," + str(commanderId) + "," + dosql(newName) + ")"
            dbQuery(query)            
            return HttpResponseRedirect('/s03/commanders/')
        
        #---
        
        elif action == 'engage':
            commanderId = ToInt(request.GET.get("id"), 0)
            query = "SELECT sp_commanders_engage(" + str(self.userId) + "," + str(commanderId) + ")"
            dbQuery(query)
            return HttpResponseRedirect('/s03/commanders/')
        
        #---
        
        elif action == 'train':
            commanderId = ToInt(request.GET.get("id"), 0)
            query = "SELECT sp_commanders_train(" + str(self.userId) + "," + str(commanderId) + ")"
            dbQuery(query)
            return HttpResponseRedirect('/s03/commanders/')
        
        #---
        
        elif action == 'fire':
            commanderId = ToInt(request.GET.get("id"), 0)
            query = "SELECT sp_commanders_fire(" + str(self.userId) + "," + str(commanderId) + ")"
            dbQuery(query)
            return HttpResponseRedirect('/s03/commanders/')
        
        #---
        
        elif action == 'skills':
            
            commanderId = ToInt(request.GET.get("id"), 0)
            
            tpl = getTemplate(request, "s03/commanders")

            query = "SELECT id, mod_production_ore, mod_production_hydrocarbon, mod_production_energy," + \
                    " mod_production_workers, mod_fleet_speed, mod_fleet_shield, mod_fleet_handling," + \
                    " mod_fleet_tracking_speed, mod_fleet_damage, mod_fleet_signature," + \
                    " mod_construction_speed_buildings, mod_construction_speed_ships," + \
                    " points, name" + \
                    " FROM commanders WHERE points > 0 AND id=" + str(commanderId) + " AND ownerid=" + str(self.userId)
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
            
            return self.display(tpl, request)
            
        #---
        
        else:
        
            dbQuery("SELECT sp_commanders_check_new_commanders(" + str(self.userId) + ")")
            
            tpl = getTemplate(request, "s03/commanders")
            
            result = dbExecute("SELECT int4(count(1)) FROM commanders WHERE recruited <= now() AND ownerid=" + str(self.userId))
            can_engage = result < self.profile["mod_commanders"]
            tpl.setValue('can_engage', can_engage)
            
            tpl.setValue("max_commanders", int(self.profile["mod_commanders"]))
            
            #---
            
            query = "SELECT c.id AS cmd_id, c.name AS cmd_name, c.recruited, points, added, salary, can_be_fired, " + \
                    " p.id AS planet_id, p.galaxy, p.sector, p.planet, p.name AS planet_name, " + \
                    " f.id AS fleet_id, f.name AS fleet_name, " + \
                    " c.mod_production_ore, c.mod_production_hydrocarbon, c.mod_production_energy, " + \
                    " c.mod_production_workers, c.mod_fleet_speed, c.mod_fleet_shield, " + \
                    " c.mod_fleet_handling, c.mod_fleet_tracking_speed, c.mod_fleet_damage, c.mod_fleet_signature, "  + \
                    " c.mod_construction_speed_buildings, c.mod_construction_speed_ships, last_training < now()-interval '1 day' AS can_train, sp_commanders_prestige_to_train(c.ownerid, c.id) AS train_cost, salary_increases >= 20 AS cant_train_anymore" + \
                    " FROM commanders AS c" + \
                    "  LEFT JOIN fleets AS f ON (c.id=f.commanderid)" + \
                    "  LEFT JOIN nav_planet AS p ON (c.id=p.commanderid)" + \
                    " WHERE c.recruited IS NOT NULL AND c.ownerid=" + str(self.userId) + \
                    " ORDER BY upper(c.name)"
            commanders = dbRows(query)
            tpl.setValue('commanders', commanders)
            
            for commander in commanders:
                
                commander['mod_production_ore'] = round((commander['mod_production_ore'] - 1.0) * 100)
                commander["mod_production_hydrocarbon"] = round((commander['mod_production_hydrocarbon'] - 1.0) * 100)
                commander["mod_production_energy"] = round((commander['mod_production_energy'] - 1.0) * 100)
                commander["mod_production_workers"] = round((commander['mod_production_workers'] - 1.0) * 100)

                commander["mod_fleet_speed"] = round((commander['mod_fleet_speed'] - 1.0) * 100)
                commander["mod_fleet_shield"] = round((commander['mod_fleet_shield'] - 1.0) * 100)
                commander["mod_fleet_handling"] = round((commander['mod_fleet_handling'] - 1.0) * 100)
                commander["mod_fleet_tracking_speed"] = round((commander['mod_fleet_tracking_speed'] - 1.0) * 100)
                commander["mod_fleet_damage"] = round((commander['mod_fleet_damage'] - 1.0) * 100)
                commander["mod_fleet_signature"] = round((commander['mod_fleet_signature'] - 1.0) * 100)

                commander["mod_construction_speed_buildings"] = round((commander['mod_construction_speed_buildings'] - 1.0) * 100)
                commander["mod_construction_speed_ships"] = round((commander['mod_construction_speed_ships'] - 1.0) * 100)
            
            #---
            
            query = "SELECT c.id AS cmd_id, c.name AS cmd_name, points, added, salary," + \
                    " c.mod_production_ore, c.mod_production_hydrocarbon, c.mod_production_energy, " + \
                    " c.mod_production_workers, c.mod_fleet_speed, c.mod_fleet_shield, " + \
                    " c.mod_fleet_handling, c.mod_fleet_tracking_speed, c.mod_fleet_damage, c.mod_fleet_signature, "  + \
                    " c.mod_construction_speed_buildings, c.mod_construction_speed_ships" + \
                    " FROM commanders AS c" + \
                    " WHERE c.recruited IS NULL AND c.ownerid=" + str(self.userId) + \
                    " ORDER BY upper(c.name)"
            available_commanders = dbRows(query)
            tpl.setValue('available_commanders', available_commanders)
            
            for commander in available_commanders:
                
                commander['mod_production_ore'] = round((commander['mod_production_ore'] - 1.0) * 100)
                commander["mod_production_hydrocarbon"] = round((commander['mod_production_hydrocarbon'] - 1.0) * 100)
                commander["mod_production_energy"] = round((commander['mod_production_energy'] - 1.0) * 100)
                commander["mod_production_workers"] = round((commander['mod_production_workers'] - 1.0) * 100)

                commander["mod_fleet_speed"] = round((commander['mod_fleet_speed'] - 1.0) * 100)
                commander["mod_fleet_shield"] = round((commander['mod_fleet_shield'] - 1.0) * 100)
                commander["mod_fleet_handling"] = round((commander['mod_fleet_handling'] - 1.0) * 100)
                commander["mod_fleet_tracking_speed"] = round((commander['mod_fleet_tracking_speed'] - 1.0) * 100)
                commander["mod_fleet_damage"] = round((commander['mod_fleet_damage'] - 1.0) * 100)
                commander["mod_fleet_signature"] = round((commander['mod_fleet_signature'] - 1.0) * 100)

                commander["mod_construction_speed_buildings"] = round((commander['mod_construction_speed_buildings'] - 1.0) * 100)
                commander["mod_construction_speed_ships"] = round((commander['mod_construction_speed_ships'] - 1.0) * 100)
            
            return self.display(tpl, request)
