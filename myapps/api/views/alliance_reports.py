# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive, HasAlliance ]

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

        tpl = getTemplate()
        
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
        rows = dbRows(query)
        
        reports = []
        tpl.set('reports', reports)
        
        for row in rows:

            reportType = row['type'] * 100 + row['subtype']
            if reportType != 140 and reportType != 141 and reportType != 142 and reportType != 133:
            
                report = row
                reports.append(report)

                report['type'] = reportType
                
        #---
        
        return Response(tpl.data)
