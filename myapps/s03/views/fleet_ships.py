# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        self.fleetId = ToInt(request.GET.get("id"), 0)
        if self.fleetId == 0: return HttpResponseRedirect("/s03/fleets/")
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        action = request.POST.get("action")
        
        #---
        
        if action == 'transfer_ships':

            shipIds = dbRows("SELECT id FROM db_ships")
            planetId = dbExecute("SELECT planetid FROM fleets WHERE id=" + str(self.fleetId))

            for shipId in shipIds:
                quantity = ToInt(request.POST.get("addship" + str(shipId['id'])), 0)
                if quantity > 0:
                    dbExecute("SELECT sp_transfer_ships_to_fleet(" + str(self.userId) + "," + str(self.fleetId) + "," + str(shipId['id']) + "," + str(quantity) + ")")


            for shipId in shipIds:
                quantity = ToInt(request.POST.get("removeship" + str(shipId['id'])), 0)
                if quantity > 0:
                    dbExecute("SELECT sp_transfer_ships_to_planet(" + str(self.userId) + "," + str(self.fleetId) + "," + str(shipId['id']) + "," + str(quantity) + ")")

            result = dbExecute("SELECT id FROM fleets WHERE id=" + str(self.fleetId))
            if result == None:
                return HttpResponseRedirect("/s03/orbit/?planet=" + str(planetId))
            
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
        
        #---
        
        return HttpResponseRedirect('/s03/fleets/')
    
    def get(self, request, *args, **kwargs):

        content = getTemplate(request, "s03/fleet-ships")

        self.selectedMenu = "fleets"

        #---
        
        query = "SELECT id, name, attackonsight, engaged, size, signature, speed, remaining_time, commanderid, commandername," + \
                " planetid, planet_name, planet_galaxy, planet_sector, planet_planet, planet_ownerid, planet_owner_name, planet_owner_relation," + \
                " cargo_capacity, cargo_load, cargo_ore, cargo_hydrocarbon, cargo_scientists, cargo_soldiers, cargo_workers" + \
                " FROM vw_fleets WHERE planet_owner_relation = 2 AND engaged = False AND remaining_time IS NULL AND ownerid=" + str(self.userId)+" AND id=" + str(self.fleetId)
        fleet = dbRow(query)
        if fleet == None: return HttpResponseRedirect("/s03/fleets/")
        content.setValue("fleet", fleet)

        #---

        query = "SELECT db_ships.id, db_ships.capacity, db_ships.label, db_ships.capacity," + \
                " COALESCE((SELECT quantity FROM fleets_ships WHERE fleetId=" + str(self.fleetId) + " AND shipId = db_ships.id), 0) AS fleet_count," + \
                " COALESCE((SELECT quantity FROM planet_ships WHERE planetid=(SELECT planetid FROM fleets WHERE id=" + str(self.fleetId) + ") AND shipId = db_ships.id), 0) AS planet_count" + \
                " FROM db_ships" + \
                " ORDER BY db_ships.category, db_ships.label"
        results = dbRows(query)
        
        ships = []
        content.setValue("ships", ships)
        
        for result in results:
            if result['fleet_count'] > 0 or result['planet_count'] > 0:
                ships.append(result)
        
        return self.display(content, request)
