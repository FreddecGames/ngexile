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
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action')
        
        #---

        if action == 'save':
        
            query = 'SELECT buildingid, (quantity - CASE WHEN destroy_datetime IS NULL THEN 0 ELSE 1 END) AS quantity, disabled' + \
                    ' FROM planet_buildings' + \
                    '    INNER JOIN db_buildings ON (planet_buildings.buildingid=db_buildings.id)' + \
                    ' WHERE can_be_disabled AND planetid=' + str(self.currentPlanetId)
            rows = dbRows(query)
            
            for row in rows:

                quantity = row['quantity'] - ToInt(request.POST.get('enabled' + str(row['buildingid'])), 0)

                query = 'UPDATE planet_buildings SET' + \
                        ' disabled=LEAST(quantity - CASE WHEN destroy_datetime IS NULL THEN 0 ELSE 1 END, ' + str(quantity) + ')' + \
                        'WHERE planetid=' + str(self.currentPlanetId) + ' AND buildingid =' + str(row['buildingid'])
                dbQuery(query)
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
    
    ################################################################################
    
    def get(self, request, *args, **kwargs):

        #---

        tpl = getTemplate(request, 'planet-working')
        
        self.selectedMenu = 'planet'

        self.showHeader = True
        self.headerUrl = '/s03/planet-working/'
            
        #---
    
        query = 'SELECT buildingid, (quantity - CASE WHEN destroy_datetime IS NULL THEN 0 ELSE 1 END) AS quantity, disabled, energy_consumption, int4(workers*maintenance_factor/100.0) AS maintenance, upkeep,' + \
                ' label' + \
                ' FROM planet_buildings' + \
                '    INNER JOIN db_buildings ON (planet_buildings.buildingid=db_buildings.id)' + \
                ' WHERE can_be_disabled AND quantity > 0 AND planetid=' + str(self.currentPlanetId) + \
                ' ORDER BY buildingid'
        rows = dbRows(query)

        tpl.set('buildings', rows)
        
        for row in rows:
            
            enabled = row['quantity'] - row['disabled']

            row['energy_total'] = round(enabled * row['energy_consumption'])
            row['upkeep_total'] = round(enabled * row['upkeep'])
            row['maintenance_total'] = round(enabled * row['maintenance'])

            row['counts'] = []
            for i in range(0, row['quantity'] + 1):
            
                data = {}
                data['count'] = i
                
                if i == enabled: data['selected'] = True
                
                row['counts'].append(data)

        #---

        return self.display(tpl, request)
        