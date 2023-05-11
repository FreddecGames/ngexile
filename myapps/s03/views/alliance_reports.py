# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    ################################################################################

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---

        if not self.allianceId or not self.hasRight('can_see_reports'):
            return HttpResponseRedirect('/s03/')
        
        #---

        return super().dispatch(request, *args, **kwargs)
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):
    
        #---

        tpl = getTemplate(request, 'alliance-reports')
        
        self.selectedMenu = 'alliance'
        
        #---

        query = 'SELECT type, subtype, datetime, battleid, fleetid, fleet_name,' + \
                ' planetid, planet_name, galaxy, sector, planet,' + \
                ' researchid, 0, read_date,' + \
                ' planet_relation, planet_ownername,' + \
                ' ore, hydrocarbon, credits, scientists, soldiers, workers, username,' + \
                ' alliance_tag, alliance_name,' + \
                ' invasionid, spyid, spy_key, description, ownerid, invited_username, login, buildingid' + \
                ' FROM vw_alliances_reports' + \
                ' WHERE ownerallianceid = ' + str(self.allianceId) + ' ORDER BY datetime DESC LIMIT 200'
        reports = dbRows(query)
        tpl.set('reports', reports)

        for report in reports:
            report['type'] = report['type'] * 100 + report['subtype']

        #---
        
        return self.display(tpl, request)
