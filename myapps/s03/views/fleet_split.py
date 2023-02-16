# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

from myapps.s03.views._utils import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "fleets"

        self.fleet_split_error = 0
        self.e_no_error = 0

        self.e_bad_name = 1
        self.e_already_exists = 2
        self.e_occupied = 3
        self.e_limit_reached = 4

        fleetid = ToInt(request.GET.get("id"), 0)

        if fleetid == 0:
            return HttpResponseRedirect("/s03/fleets/")

        response = self.ExecuteOrder(fleetid)
        if response: return response
        
        return self.DisplayExchangeForm(fleetid)

    # display fleet info
    def DisplayExchangeForm(self, fleetid):

        content = getTemplate(self.request, "s03/fleet-split")

        # retrieve fleet name, size, position, destination
        query = "SELECT id, name, attackonsight, engaged, size, signature, speed, remaining_time, commanderid, commandername," + \
                " planetid, planet_name, planet_galaxy, planet_sector, planet_planet, planet_ownerid, planet_owner_name, planet_owner_relation," + \
                " cargo_capacity, cargo_ore, cargo_hydrocarbon, cargo_scientists, cargo_soldiers, cargo_workers," + \
                " action " + \
                " FROM vw_fleets" + \
                " WHERE ownerid="+str(self.userId)+" AND id="+str(fleetid)

        oRs = oConnExecute(query)

        # if fleet doesn't exist, redirect to the list of fleets
        if oRs == None:
            return HttpResponseRedirect("/s03/fleets/")

        # if fleet is moving or engaged, go back to the fleets
        if oRs[24] != 0:
            return HttpResponseRedirect("/s03/fleet/?id=" + str(fleetid))

        content.setValue("fleetid", fleetid)
        content.setValue("fleetname", oRs[1])
        content.setValue("size", oRs[4])
        content.setValue("speed", oRs[6])

        content.setValue("fleet_capacity", oRs[18])
        content.setValue("available_ore", oRs[19])
        content.setValue("available_hydrocarbon", oRs[20])
        content.setValue("available_scientists", oRs[21])
        content.setValue("available_soldiers", oRs[22])
        content.setValue("available_workers", oRs[23])

        content.setValue("fleet_load", oRs[19] + oRs[20] + oRs[21] + oRs[22] + oRs[23])

        shipCount = 0
        # retrieve the list of ships in the fleet
        query = "SELECT db_ships.id, db_ships.label, db_ships.capacity, db_ships.signature," + \
                    "COALESCE((SELECT quantity FROM fleets_ships WHERE fleetid=" + str(fleetid) + " AND shipid = db_ships.id), 0)" + \
                " FROM fleets_ships" + \
                "    INNER JOIN db_ships ON (db_ships.id=fleets_ships.shipid)" + \
                " WHERE fleetid=" + str(fleetid) + \
                " ORDER BY db_ships.category, db_ships.label"

        oRss = oConnExecuteAll(query)

        list = []
        content.setValue("ships", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            shipCount = shipCount + 1
            item["id"] = oRs[0]
            item["name"] = oRs[1]
            item["cargo_capacity"] = oRs[2]
            item["signature"] = oRs[3]
            item["quantity"] = oRs[4]

            if self.fleet_split_error != self.e_no_error:
                item["transfer"] = self.request.POST.get("transfership"+str(oRs[0]))

        if self.fleet_split_error != self.e_no_error:
            content.Parse("error"+str(self.fleet_split_error))
            item["t_ore"] = self.request.POST.get("load_ore")
            item["t_hydrocarbon"] = self.request.POST.get("load_hydrocarbon")
            item["t_scientists"] = self.request.POST.get("load_scientists")
            item["t_workers"] = self.request.POST.get("load_workers")
            item["t_soldiers"] = self.request.POST.get("load_soldiers")

        return self.display(content)

    # split current fleet into 2 fleets
    def SplitFleet(self, fleetid):

        newfleetname = self.request.POST.get("newname")

        if not isValidObjectName(newfleetname):
            self.fleet_split_error = self.e_bad_name
            return

        #
        # retrieve the planet where the current fleet is patrolling
        #
        query = "SELECT planetid FROM vw_fleets WHERE ownerid="+str(self.userId)+" AND id="+str(fleetid)
        oRs = oConnExecute(query)
        if oRs == None: return

        fleetplanetid = int(oRs[0])

        #
        # retrieve 'source' fleet cargo and action
        #
        query = " SELECT id, action, cargo_ore, cargo_hydrocarbon, " + \
                " cargo_scientists, cargo_soldiers, cargo_workers" + \
                " FROM vw_fleets" + \
                " WHERE ownerid="+str(self.userId)+" AND id="+str(fleetid)
        oRs = oConnExecute(query)

        if oRs == None or (oRs[1] != 0):
            self.fleet_split_error = self.e_occupied
            return

        ore = min( ToInt(self.request.POST.get("load_ore"), 0), oRs[2] )
        hydrocarbon = min( ToInt(self.request.POST.get("load_hydrocarbon"), 0), oRs[3] )
        scientists = min( ToInt(self.request.POST.get("load_scientists"), 0), oRs[4] )
        soldiers = min( ToInt(self.request.POST.get("load_soldiers"), 0), oRs[5] )
        workers = min( ToInt(self.request.POST.get("load_workers"), 0), oRs[6] )

        #
        # begin transaction
        #
        #
        # 1/ create a new fleet at the current fleet planet with the given name
        #
        oRs = oConnExecute("SELECT sp_create_fleet(" + str(self.userId) + "," + str(fleetplanetid) + "," + dosql(newfleetname) + ")")
        if oRs == None:
            return

        newfleetid = int(oRs[0])

        if newfleetid < 0:
            if newfleetid == -1:
                self.fleet_split_error = self.e_already_exists

            if newfleetid == -2:
                self.fleet_split_error = self.e_already_exists

            if newfleetid == -3:
                self.fleet_split_error = self.e_limit_reached

            return

        #
        # 2/ add the ships to the new fleet
        #

        # retrieve ships belonging to current fleet
        query = "SELECT db_ships.id, " + \
                    "COALESCE((SELECT quantity FROM fleets_ships WHERE fleetid=" + str(fleetid) + " AND shipid = db_ships.id), 0)" + \
                " FROM db_ships" + \
                " ORDER BY db_ships.category, db_ships.label"
        availableArray = oConnExecuteAll(query)

        # for each available ship id, check if the player wants to add ships of this kind
        for i in availableArray:
            shipid = i[0]

            quantity = min( ToInt(self.request.POST.get("transfership" + str(shipid)), 0), i[1] )

            if quantity > 0:
                # add the ships to the new fleet
                query = " INSERT INTO fleets_ships (fleetid, shipid, quantity)" + \
                        " VALUES (" + str(newfleetid) +","+ str(shipid) +","+ str(quantity) + ")"
                oConnDoQuery(query)

        # reset fleets idleness, partly to prevent cheating and being able to do multiple invasions with only a fleet
        oConnDoQuery("UPDATE fleets SET idle_since=now()" + \
                        " WHERE ownerid =" + str(self.userId) + " AND (id="+str(newfleetid)+" OR id="+str(fleetid)+")")

        #
        # 3/ Move the resources to the new fleet
        #   a/ Add resources to the new fleet
        #
        
        # retrieve new fleet's cargo capacity
        oRs = oConnExecute("SELECT cargo_capacity FROM vw_fleets WHERE ownerid="+str(self.userId)+" AND id="+str(newfleetid))
        if oRs == None:
                return

        newload = oRs[0]

        ore = min( ore, newload)
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
            # a/ put the resources to the new fleet
            oConnDoQuery("UPDATE fleets SET" + \
                        " cargo_ore="+str(ore)+", cargo_hydrocarbon="+str(hydrocarbon)+", " + \
                        " cargo_scientists="+str(scientists)+", cargo_soldiers="+str(soldiers)+", " + \
                        " cargo_workers="+str(workers) + \
                        " WHERE id =" + str(newfleetid) + " AND ownerid =" + str(self.userId))

        #
        # 1a/ Remove resource from the 'source# fleet
        #

        if ore != 0 or hydrocarbon != 0 or scientists != 0 or soldiers != 0 or workers != 0:

            # a/ remove the resources from the 'source# fleet
            oConnDoQuery("UPDATE fleets SET" + \
                        " cargo_ore=cargo_ore-"+str(ore)+", cargo_hydrocarbon=cargo_hydrocarbon-"+str(hydrocarbon)+", " + \
                        " cargo_scientists=cargo_scientists-"+str(scientists)+", " + \
                        " cargo_soldiers=cargo_soldiers-"+str(soldiers)+", " + \
                        " cargo_workers=cargo_workers-"+str(workers) + \
                        " WHERE id =" + str(fleetid) + " AND ownerid =" + str(self.userId))
                        
                        
        #
        # 4/ Remove the ships from the 'source# fleet
        #
        for i in availableArray:
            shipid = i[0]

            quantity = min( ToInt(self.request.POST.get("transfership" + str(shipid)), 0), i[1] )

            if quantity > 0:
                # remove the ships from the 'source# fleet
                query = " UPDATE fleets_ships SET" + \
                        " quantity=quantity-" + str(quantity) + \
                        " WHERE fleetid=" + str(fleetid) + " AND shipid=" + str(shipid)
                oConnDoQuery(query)

        query = "DELETE FROM fleets WHERE ownerid=" + str(self.userId) + " AND size=0"
        oConnDoQuery(query)

        return HttpResponseRedirect("/s03/fleet/?id="+str(newfleetid))

    def ExecuteOrder(self, fleetid):
        if self.request.POST.get("split") == "1":
            return self.SplitFleet(fleetid)
