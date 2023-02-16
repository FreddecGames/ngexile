# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

from myapps.s03.views._utils import *

class View(GlobalView):
    
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        self.selectedMenu = "fleets"
        
        self.can_command_alliance_fleets = -1
        
        if self.allianceId and self.hasRight("can_order_other_fleets"):
            self.can_command_alliance_fleets = self.allianceId
        
        self.fleet_owner_id = self.userId
        
        self.fleetid = ToInt(self.request.GET.get("id"), 0)
        
        if self.fleetid == 0:
            return HttpResponseRedirect("/s03/fleets/")
        
        if not self.RetrieveFleetOwnerId(self.fleetid):
            return HttpResponseRedirect("/s03/fleets/")
        
        self.TransferResourcesViaPost(self.fleetid)
        
        if self.request.GET.get("a") != "open":
            return HttpResponseRedirect("/s03/fleet/?id=" + str(self.fleetid))
        
        self.TransferResources(self.fleetid)
        
        return self.DisplayExchangeForm(self.fleetid)
    
    def RetrieveFleetOwnerId(self, fleetid):
    
        # retrieve fleet owner
        query = "SELECT ownerid" +\
                " FROM vw_fleets as f" +\
                " WHERE (ownerid=" + str(self.userId) + " OR (shared AND owner_alliance_id=" + str(self.can_command_alliance_fleets) + ")) AND id=" + str(self.fleetid)
        oRs = oConnExecute(query)
        if oRs:
            self.fleet_owner_id = oRs[0]
            return True
        else: return False
    
    # display fleet info
    def DisplayExchangeForm(self, fleetid):
        content = getTemplate(self.request, "s03/fleet-trade")
    
        # retrieve fleet name, size, position, destination
        query = "SELECT id, name, attackonsight, engaged, size, signature, speed, remaining_time, commanderid, commandername," +\
                " planetid, planet_name, planet_galaxy, planet_sector, planet_planet, planet_ownerid, planet_owner_name, planet_owner_relation," +\
                " cargo_capacity, cargo_ore, cargo_hydrocarbon, cargo_scientists, cargo_soldiers, cargo_workers" + \
                " FROM vw_fleets" +\
                " WHERE ownerid=" + str(self.fleet_owner_id) + " AND id="+str(self.fleetid)
        oRs = oConnExecute(query)
    
        # if fleet doesn't exist, redirect to the list of fleets
        if oRs == None:
            if self.request.GET.get("a") == "open":
                return HttpResponseRedirect("/s03/fleets/")
            else:
                return HttpResponseRedirect("/s03/fleets/")
    
        relation = oRs[17]
    
        # if fleet is moving or engaged, go back to the fleets
        if oRs[7] or oRs[3]:
            if self.request.GET.get("a") == "open":
                relation = rWar
            else:
                return HttpResponseRedirect("/s03/fleet/?id=" + str(self.fleetid))
            
        content.setValue("fleetid", self.fleetid)
        content.setValue("fleetname", oRs[1])
        content.setValue("size", oRs[4])
        content.setValue("speed", oRs[6])
    
        content.setValue("fleet_capacity", oRs[18])
        content.setValue("fleet_ore", oRs[19])
        content.setValue("fleet_hydrocarbon", oRs[20])
        content.setValue("fleet_scientists", oRs[21])
        content.setValue("fleet_soldiers", oRs[22])
        content.setValue("fleet_workers", oRs[23])
    
        content.setValue("fleet_load", oRs[19] + oRs[20] + oRs[21] + oRs[22] + oRs[23])
    
        if relation == rSelf:
            # retrieve planet ore, hydrocarbon, workers, relation
            query = "SELECT ore, hydrocarbon, scientists, soldiers," +\
                    " GREATEST(0, workers-GREATEST(workers_busy,workers_for_maintenance-workers_for_maintenance/2+1,500))," +\
                    " workers > workers_for_maintenance/2" +\
                    " FROM vw_planets WHERE id="+str(oRs[10])
            oRs = oConnExecute(query)

            content.setValue("planet_ore", oRs[0])
            content.setValue("planet_hydrocarbon", oRs[1])
            content.setValue("planet_scientists", oRs[2])
            content.setValue("planet_soldiers", oRs[3])
            content.setValue("planet_workers", oRs[4])

            if not oRs[5]:
                content.setValue("planet_ore", 0)
                content.setValue("planet_hydrocarbon", 0)
                content.Parse("not_enough_workers_to_load")

            content.Parse("load")
        elif relation in [rFriend, rAlliance, rHostile]:

            content.Parse("unload")
        else:
            content.Parse("cargo")
    
        return self.display(content)
    
    def TransferResources(self, fleetid):
    
        ore = ToInt(self.request.GET.get("load_ore"), 0) - ToInt(self.request.GET.get("unload_ore"), 0)
        hydrocarbon = ToInt(self.request.GET.get("load_hydrocarbon"), 0) - ToInt(self.request.GET.get("unload_hydrocarbon"), 0)
        scientists = ToInt(self.request.GET.get("load_scientists"), 0) - ToInt(self.request.GET.get("unload_scientists"), 0)
        soldiers = ToInt(self.request.GET.get("load_soldiers"), 0) - ToInt(self.request.GET.get("unload_soldiers"), 0)
        workers = ToInt(self.request.GET.get("load_workers"), 0) - ToInt(self.request.GET.get("unload_workers"), 0)
    
        if ore != 0 or hydrocarbon != 0 or scientists != 0 or soldiers != 0 or workers != 0:
            oRs = oConnExecute("SELECT sp_transfer_resources_with_planet(" + str(self.fleet_owner_id) + "," + str(self.fleetid) + "," + str(ore) + "," + str(hydrocarbon) + "," + str(scientists) + "," + str(soldiers) + "," + str(workers) + ")")
    
    def TransferResourcesViaPost(self, fleetid):
    
        ore = ToInt(self.request.POST.get("load_ore"), 0) - ToInt(self.request.POST.get("unload_ore"), 0)
        hydrocarbon = ToInt(self.request.POST.get("load_hydrocarbon"), 0) - ToInt(self.request.POST.get("unload_hydrocarbon"), 0)
        scientists = ToInt(self.request.POST.get("load_scientists"), 0) - ToInt(self.request.POST.get("unload_scientists"), 0)
        soldiers = ToInt(self.request.POST.get("load_soldiers"), 0) - ToInt(self.request.POST.get("unload_soldiers"), 0)
        workers = ToInt(self.request.POST.get("load_workers"), 0) - ToInt(self.request.POST.get("unload_workers"), 0)
    
        if ore != 0 or hydrocarbon != 0 or scientists != 0 or soldiers != 0 or workers != 0:
            oRs = oConnExecute("SELECT sp_transfer_resources_with_planet(" + str(self.fleet_owner_id) + "," + str(self.fleetid) + "," + str(ore) + "," + str(hydrocarbon) + "," + str(scientists) + "," + str(soldiers) + "," + str(workers) + ")")
            return HttpResponseRedirect("/s03/fleet/?id=" + str(self.fleetid) + "+trade=" + str(oRs[0]))
