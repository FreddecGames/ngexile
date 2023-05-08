# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        #---

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
        
        if action == 'split':

            newfleetname = request.POST.get("newname")
            if not isValidObjectName(newfleetname):
                messages.error(request, 'error_badname')
                return HttpResponseRedirect('/s03/fleet-split/?id=' + str(self.fleetId))
            
            #---
            
            query = "SELECT id, planetid, action, cargo_ore, cargo_hydrocarbon," + \
                    " cargo_scientists, cargo_soldiers, cargo_workers" + \
                    " FROM vw_fleets" + \
                    " WHERE action=0 AND ownerid=" + str(self.userId) + " AND id=" + str(self.fleetId)
            fleet = dbRow(query)
            
            if fleet == None:
                messages.error(request, 'error_occupied')
                return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
                
            #---

            newfleetid = dbExecute("SELECT sp_create_fleet(" + str(self.userId) + "," + str(fleet['planetid']) + "," + dosql(newfleetname) + ")")
            if newfleetid < 0:
                if newfleetid == -1: messages.error(request, 'error_already_exists')
                elif newfleetid == -2: messages.error(request, 'error_already_exists')
                elif newfleetid == -3: messages.error(request, 'error_limit_reached')
                return HttpResponseRedirect('/s03/fleet-split/?id=' + str(self.fleetId))
            
            #---
            
            query = "SELECT db_ships.id, " + \
                    " COALESCE((SELECT quantity FROM fleets_ships WHERE fleetId=" + str(self.fleetId) + " AND shipid = db_ships.id), 0) AS count" + \
                    " FROM db_ships" + \
                    " ORDER BY db_ships.category, db_ships.label"
            ships = dbRows(query)
            
            for ship in ships:            
                quantity = min(ToInt(request.POST.get("transfership" + str(ship['id'])), 0), ship['count'])
                if quantity > 0:
                    query = "INSERT INTO fleets_ships(fleetId, shipid, quantity) VALUES(" + str(newfleetid) + "," + str(ship['id']) +"," + str(quantity) + ")"
                    dbQuery(query)

            #---
                    
            dbQuery("UPDATE fleets SET idle_since=now() WHERE ownerid =" + str(self.userId) + " AND (id=" + str(newfleetid) + " OR id=" + str(self.fleetId) + ")")

            #---
            
            newload = dbExecute("SELECT cargo_capacity FROM vw_fleets WHERE ownerid=" + str(self.userId) + " AND id=" + str(newfleetid))
            
            ore = max(min(ToInt(request.POST.get("load_ore"), 0), fleet['cargo_ore']), 0)
            hydrocarbon = max(min(ToInt(request.POST.get("load_hydrocarbon"), 0), fleet['cargo_hydrocarbon']), 0)
            scientists = max(min(ToInt(request.POST.get("load_scientists"), 0), fleet['cargo_scientists']), 0)
            soldiers = max(min(ToInt(request.POST.get("load_soldiers"), 0), fleet['cargo_soldiers']), 0)
            workers = max(min(ToInt(request.POST.get("load_workers"), 0), fleet['cargo_workers']), 0)

            ore = min(ore, newload)
            newload = newload - ore

            hydrocarbon = min( hydrocarbon, newload)
            newload = newload - hydrocarbon

            scientists = min( scientists, newload)
            newload = newload - scientists

            soldiers = min( soldiers, newload)
            newload = newload - soldiers

            workers = min( workers, newload)
            newload = newload - workers

            if ore != 0 or hydrocarbon != 0 or scientists != 0 or soldiers != 0 or workers != 0:

                dbQuery("UPDATE fleets SET" + \
                        " cargo_ore=" + str(ore) + ", cargo_hydrocarbon=" + str(hydrocarbon) + ", " + \
                        " cargo_scientists=" + str(scientists) + ", cargo_soldiers=" + str(soldiers) + ", " + \
                        " cargo_workers=" + str(workers) + \
                        " WHERE id =" + str(newfleetid) + " AND ownerid =" + str(self.userId))

                dbQuery("UPDATE fleets SET" + \
                        " cargo_ore=cargo_ore-" + str(ore) + ", cargo_hydrocarbon=cargo_hydrocarbon-" + str(hydrocarbon) + ", " + \
                        " cargo_scientists=cargo_scientists-" + str(scientists) + ", " + \
                        " cargo_soldiers=cargo_soldiers-" + str(soldiers) + ", " + \
                        " cargo_workers=cargo_workers-" + str(workers) + \
                        " WHERE id =" + str(self.fleetId) + " AND ownerid =" + str(self.userId))

            #---
                            
            for ship in ships:
                quantity = min(ToInt(request.POST.get("transfership" + str(ship['id'])), 0), ship['count'])
                if quantity > 0:
                    query = " UPDATE fleets_ships SET quantity=quantity-" + str(quantity) + " WHERE fleetId=" + str(self.fleetId) + " AND shipid=" + str(ship['id'])
                    dbQuery(query)

            #---
           
            query = "DELETE FROM fleets WHERE ownerid=" + str(self.userId) + " AND size=0"
            dbQuery(query)

            return HttpResponseRedirect("/s03/fleet/?id=" + str(newfleetid))
        
        #---
        
        return HttpResponseRedirect('/s03/fleets/')
    
    def get(self, request, *args, **kwargs):

        content = getTemplate(request, "s03/fleet-split")

        self.selectedMenu = "fleets"

        #---

        query = "SELECT id, name, attackonsight, engaged, size, signature, speed, remaining_time, commanderid, commandername," + \
                " planetid, planet_name, planet_galaxy, planet_sector, planet_planet, planet_ownerid, planet_owner_name, planet_owner_relation," + \
                " cargo_capacity, cargo_load, cargo_ore, cargo_hydrocarbon, cargo_scientists, cargo_soldiers, cargo_workers," + \
                " action " + \
                " FROM vw_fleets" + \
                " WHERE action=0 AND ownerid=" + str(self.userId) + " AND id=" + str(self.fleetId)
        fleet = dbRow(query)
        if fleet == None: return HttpResponseRedirect("/s03/fleets/")
        content.setValue("fleet", fleet)

        #---

        query = "SELECT db_ships.id, db_ships.label, db_ships.capacity, db_ships.signature, db_ships.label," + \
                    "COALESCE((SELECT quantity FROM fleets_ships WHERE fleetId=" + str(self.fleetId) + " AND shipid = db_ships.id), 0) AS count" + \
                " FROM fleets_ships" + \
                "    INNER JOIN db_ships ON (db_ships.id=fleets_ships.shipid)" + \
                " WHERE fleetId=" + str(self.fleetId) + \
                " ORDER BY db_ships.category, db_ships.label"
        ships = dbRows(query)
        content.setValue("ships", ships)
        
        #---
         
        return self.display(content, request)
