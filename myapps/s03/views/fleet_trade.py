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
        
        return HttpResponseRedirect("/s03/fleet/?id=" + str(self.fleetid))
    
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
        
    def TransferResourcesViaPost(self, fleetid):
    
        ore = ToInt(self.request.POST.get("load_ore"), 0) - ToInt(self.request.POST.get("unload_ore"), 0)
        hydrocarbon = ToInt(self.request.POST.get("load_hydrocarbon"), 0) - ToInt(self.request.POST.get("unload_hydrocarbon"), 0)
        scientists = ToInt(self.request.POST.get("load_scientists"), 0) - ToInt(self.request.POST.get("unload_scientists"), 0)
        soldiers = ToInt(self.request.POST.get("load_soldiers"), 0) - ToInt(self.request.POST.get("unload_soldiers"), 0)
        workers = ToInt(self.request.POST.get("load_workers"), 0) - ToInt(self.request.POST.get("unload_workers"), 0)
    
        if ore != 0 or hydrocarbon != 0 or scientists != 0 or soldiers != 0 or workers != 0:
            oRs = oConnExecute("SELECT sp_transfer_resources_with_planet(" + str(self.fleet_owner_id) + "," + str(self.fleetid) + "," + str(ore) + "," + str(hydrocarbon) + "," + str(scientists) + "," + str(soldiers) + "," + str(workers) + ")")
            return HttpResponseRedirect("/s03/fleet/?id=" + str(self.fleetid) + " +trade=" + str(oRs[0]))
