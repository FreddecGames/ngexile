# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    ################################################################################
    
    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        self.invasionId = ToInt(request.GET.get('id'), 0)
        if self.invasionId == 0:
            return HttpResponseRedirect('/s03/')
        
        #---
        
        return super().dispatch(request, *args, **kwargs)
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---

        tpl = getTemplate(request, 'report-invasion')
        
        self.selectedMenu = 'reports'
        
        #---
        
        query = 'SELECT i.id, i.time, i.planet_id, i.planet_name, i.attacker_name, i.defender_name, ' + \
                ' i.attacker_succeeded, i.soldiers_total, i.soldiers_lost, i.def_soldiers_total, ' + \
                ' i.def_soldiers_lost, i.def_scientists_total, i.def_scientists_lost, i.def_workers_total, ' + \
                ' i.def_workers_lost, galaxy, sector, planet' + \
                ' FROM invasions AS i INNER JOIN nav_planet ON nav_planet.id = i.planet_id WHERE i.id = ' + str(self.invasionId)
        report = dbRow(query)
        if report == None: return HttpResponseRedirect('/s03/empire-view/')
        tpl.set('report', report)
        
        viewername = self.profile['username']
        if report['attacker_name'] != viewername and report['defender_name'] != viewername:
            if self.allianceId and self.allianceRights['can_see_reports']:

                query = 'SELECT username' + \
                        ' FROM users' + \
                        ' WHERE (username=' + dosql(report['attacker_name']) + ' OR username=' + dosql(report['defender_name']) + ') AND alliance_id=' + str(self.allianceId) + ' AND alliance_joined <= (SELECT time FROM invasions WHERE id=' + str(self.invasionId) + ')'
                result = dbExecute(query)
                if result == None: return HttpResponseRedirect('/s03/empire-view/')            
                viewername = result
                
            else: return HttpResponseRedirect('/s03/empire-view/')
        
        tpl.set('soldiers_alive', report['soldiers_total'] - report['soldiers_lost'])
        tpl.set('def_soldiers_alive', report['def_soldiers_total'] - report['def_soldiers_lost'])
        
        if report['attacker_name'] == viewername:
        
            tpl.set('relation', rWar)
            tpl.set('planetname', report['defender_name'])
            
            if report['def_soldiers_total'] - report['def_soldiers_lost'] == 0:
            
                tpl.set('def_workers_alive', report['def_workers_total'] - report['def_workers_lost'])
                tpl.set('workers')
            
                if report['def_workers_lost'] - report['def_workers_total'] == 0:
                
                    tpl.set('def_scientists_alive', report['def_scientists_total'] - report['def_scientists_lost'])
                    tpl.set('scientists')

        else:
        
            tpl.set('relation', rFriend)

            tpl.set('def_workers_alive', report['def_workers_total'] - report['def_workers_lost'])
            tpl.set('workers')

            tpl.set('def_scientists_alive', report['def_scientists_total'] - report['def_scientists_lost'])
            tpl.set('scientists')

        #---
        
        return self.display(tpl, request)
