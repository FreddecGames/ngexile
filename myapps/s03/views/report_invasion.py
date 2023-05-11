# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    ################################################################################
    
    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        return super().dispatch(request, *args, **kwargs)
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):

        #---
        
        invasionId = ToInt(request.GET.get("id"), 0)
        if invasionId == 0: return HttpResponseRedirect("/s03/empire-view/")
        
        #---

        content = getTemplate(request, "s03/invasion")
        
        self.selectedMenu = "invasion"
        
        #---
        
        query = "SELECT i.id, i.time, i.planet_id, i.planet_name, i.attacker_name, i.defender_name, " + \
                " i.attacker_succeeded, i.soldiers_total, i.soldiers_lost, i.def_soldiers_total, " + \
                " i.def_soldiers_lost, i.def_scientists_total, i.def_scientists_lost, i.def_workers_total, " + \
                " i.def_workers_lost, galaxy, sector, planet" + \
                " FROM invasions AS i INNER JOIN nav_planet ON nav_planet.id = i.planet_id WHERE i.id = " + str(invasionId)
        report = dbRow(query)
        if report == None: return HttpResponseRedirect("/s03/empire-view/")
        content.setValue("report", report)
        
        viewername = self.profile['username']
        if report['attacker_name'] != viewername and report['defender_name'] != viewername:
            if self.allianceId and self.allianceRights["can_see_reports"]:

                query = "SELECT username" + \
                        " FROM users" + \
                        " WHERE (username=" + dosql(report['attacker_name']) + " OR username=" + dosql(report['defender_name']) + ") AND alliance_id=" + str(self.allianceId) + " AND alliance_joined <= (SELECT time FROM invasions WHERE id=" + str(invasionId) + ")"
                result = dbExecute(query)
                if result == None: return HttpResponseRedirect("/s03/empire-view/")            
                viewername = result
                
            else: return HttpResponseRedirect("/s03/empire-view/")
        
        content.setValue("soldiers_alive", report['soldiers_total'] - report['soldiers_lost'])
        content.setValue("def_soldiers_alive", report['def_soldiers_total'] - report['def_soldiers_lost'])
        
        if report['attacker_name'] == viewername:
        
            content.setValue("relation", rWar)
            content.setValue("planetname", report['defender_name'])
            
            if report['def_soldiers_total'] - report['def_soldiers_lost'] == 0:
            
                content.setValue("def_workers_alive", report['def_workers_total'] - report['def_workers_lost'])
                content.Parse("workers")
            
                if report['def_workers_lost'] - report['def_workers_total'] == 0:
                
                    content.setValue("def_scientists_alive", report['def_scientists_total'] - report['def_scientists_lost'])
                    content.Parse("scientists")

        else:
        
            content.setValue("relation", rFriend)

            content.setValue("def_workers_alive", report['def_workers_total'] - report['def_workers_lost'])
            content.Parse("workers")

            content.setValue("def_scientists_alive", report['def_scientists_total'] - report['def_scientists_lost'])
            content.Parse("scientists")

        #---
        
        return self.display(content, request)
