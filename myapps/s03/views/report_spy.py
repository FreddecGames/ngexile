# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    ################################################################################
    
    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        #---
        
        reportId = ToInt(request.GET.get('id'), 0)
        if reportId == 0:
            return HttpResponseRedirect('/s03/')

        key = request.GET.get('key', '')
        if key == '':
            return HttpResponseRedirect('/s03/')
        
        #---

        query = 'SELECT id, key, userid, type, level, date, credits, spotted, target_name' + \
                ' FROM spy' + \
                ' WHERE id=' + str(reportId)+ ' AND key=' + dosql(key)
        self.report = dbRow(query)
        
        if self.report == None:
            return HttpResponseRedirect('/s03/')
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---
        
        tpl = getTemplate(request, 'report-spy')
        
        self.selectedMenu = 'intelligence'
        
        #---
        
        tpl.set('report', self.report)
        
        #---
        
        if self.report['type'] == 1:
            
            #---
            
            query = 'SELECT spy_id, planet_id, planet_name, spy_planet.floor, spy_planet.space, ground, galaxy, sector, planet, spy_planet.pct_ore, spy_planet.pct_hydrocarbon' + \
                    ' FROM spy_planet' + \
                    ' LEFT JOIN nav_planet' + \
                    '  ON (spy_planet.planet_id=nav_planet.id)' + \
                    ' WHERE spy_id=' + str(self.report['id'])
            planets = dbRows(query)
            tpl.set('planets', planets)
            
            #---
            
            query = 'SELECT category, db_research.label, research_level, levels' + \
                    ' FROM spy_research' + \
                    ' LEFT JOIN db_research' + \
                    '  ON (spy_research.research_id=db_research.id)' + \
                    ' WHERE spy_id=' + str(self.report['id']) + \
                    ' ORDER BY category, db_research.id'
            researches = dbRows(query)
            tpl.set('researches', researches)
            
            categories = []
            tpl.set('categories', categories)
            
            lastCategory = -1
            for research in researches:
            
                if research['category'] != lastCategory:
                
                    cat = { 'researches':[] }
                    categories.append(cat) 
                    
                    lastCategory = research['category']
                
                cat['researches'].append(research)            
        
        #---
        
        elif self.report['type'] == 3:
        
            #---
        
            query = 'SELECT spy_id,  planet_id,  planet_name,  s.owner_name,  s.floor,  s.space,  s.ground,  s.ore,  s.hydrocarbon,  s.ore_capacity,' + \
                    ' s.hydrocarbon_capacity,  s.ore_production,  s.hydrocarbon_production,  s.energy_consumption,  s.energy_production,  s.workers,  s.workers_capacity,  s.scientists,' + \
                    ' s.scientists_capacity,  s.soldiers,  s.soldiers_capacity,  s.radar_strength,  s.radar_jamming,  s.orbit_ore,' + \
                    ' s.orbit_hydrocarbon, galaxy, sector, planet, s.pct_ore, s.pct_hydrocarbon' + \
                    ' FROM spy_planet AS s' + \
                    ' LEFT JOIN nav_planet' + \
                    '  ON (s.planet_id=nav_planet.id)' + \
                    ' WHERE spy_id=' + str(self.report['id'])
            planet = dbRow(query)
            tpl.set('planet', planet)
            
            #---
            
            query = 'SELECT s.building_id, s.quantity, label' + \
                    ' FROM spy_building AS s' + \
                    ' LEFT JOIN db_buildings' + \
                    '  ON (s.building_id=id)' + \
                    ' WHERE spy_id=' + str(self.report['id']) + ' AND planet_id=' + str(planet['planet_id']) + ' AND s.endtime IS NULL' + \
                    ' ORDER BY category, label'
            buildings = dbRows(query)
            tpl.set('buildings', buildings)
            
            #---
            
            query = ' SELECT s.building_id, s.quantity, label, s.endtime, category' + \
                    ' FROM spy_building AS s' + \
                    ' LEFT JOIN db_buildings' + \
                    '  ON (s.building_id=id)' + \
                    ' WHERE spy_id=' + str(self.report['id']) + ' AND planet_id=' + str(planet['planet_id']) + ' AND s.endtime IS NOT NULL' + \
                    ' ORDER BY category, label'
            pendings = dbRows(query)
            tpl.set('pendings', pendings)
            
        #---
        
        return self.display(tpl, request)
