# -*- coding: utf-8 -*-

from myapps.api.views._utils import *

#---

class View(BaseView):
    permission_classes = [ IsAuthenticated ]

    ################################################################################

    def get(self, request, format=None):
        
        tpl = getTemplate()
        
        #---
        
        tpl.set('profile_credits', self.profile['credits'])
        tpl.set('profile_prestige_points', self.profile['prestige_points'])
        tpl.set('profile_alliance_id', self.allianceId)
        
        #---
        
        if self.allianceRights:
        
            if self.hasRight('can_manage_description') or self.hasRight('can_manage_announce'): tpl.set('show_management')
            if self.hasRight('can_see_reports'): tpl.set('show_reports')
            if self.hasRight('can_see_members_info'): tpl.set('show_members')
            
        #---
        
        if self.showHeader == True:
            
            query = 'SELECT ore, ore_production, ore_capacity, mod_production_ore,' + \
                    ' hydrocarbon, hydrocarbon_production, hydrocarbon_capacity, mod_production_hydrocarbon,' + \
                    ' energy, energy_consumption, energy_production, energy_capacity,' + \
                    ' workers, workers_busy, workers_capacity, workers_for_maintenance,' + \
                    ' scientists, scientists_capacity,' + \
                    ' soldiers, soldiers_capacity,' + \
                    ' floor_occupied, floor,' + \
                    ' space_occupied, space' + \
                    ' FROM vw_planets WHERE id=' + str(self.currentPlanetId)
            currentPlanet = dbRow(query)
            tpl.set('currentPlanet', currentPlanet)
        
            currentPlanet['ore_level'] = getPercent(currentPlanet['ore'], currentPlanet['ore_capacity'], 10)
            if currentPlanet['mod_production_ore'] < 0 or currentPlanet['workers'] < currentPlanet['workers_for_maintenance']: tpl.set('medium_ore_production')
            
            currentPlanet['hydrocarbon_level'] = getPercent(currentPlanet['hydrocarbon'], currentPlanet['hydrocarbon_capacity'], 10)
            if currentPlanet['mod_production_hydrocarbon'] < 0 or currentPlanet['workers'] < currentPlanet['workers_for_maintenance']: tpl.set('medium_hydrocarbon_production')
            
            currentPlanet['workers_idle'] = currentPlanet['workers'] - currentPlanet['workers_busy']  
            if currentPlanet['workers'] < currentPlanet['workers_for_maintenance']: tpl.set('workers_low')
        
            if currentPlanet['soldiers'] * 250 < currentPlanet['workers'] + currentPlanet['scientists']: tpl.set('soldiers_low')
            
            currentPlanet['energy_production'] -= currentPlanet['energy_consumption']
            
            #---
            
            tpl.set('url', self.headerUrl + '?planet=')

            #---
            
            query = 'SELECT id, name, galaxy, sector, planet' + \
                    ' FROM nav_planet' + \
                    ' WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=' + str(self.userId) + \
                    ' ORDER BY id'
            planets = dbRows(query)
            tpl.set('planets', planets)
        
            #---
            
            query = 'SELECT label' + \
                    ' FROM planet_buildings INNER JOIN db_buildings ON (db_buildings.id=buildingid AND db_buildings.is_planet_element)' + \
                    ' WHERE planetid=' + str(self.currentPlanetId) + \
                    ' ORDER BY upper(db_buildings.label)'
            specials = dbRows(query)
            tpl.set('specials', specials)
            
            #---
            
            tpl.set('header')
        
        #---
        
        query = 'SELECT (SELECT int4(COUNT(*)) FROM messages WHERE ownerid=' + str(self.userId) + ' AND read_date is NULL) AS new_mail,' + \
                '(SELECT int4(COUNT(*)) FROM reports WHERE ownerid=' + str(self.userId) + ' AND read_date is NULL AND datetime <= now()) AS new_report'
        row = dbRow(query)
        
        tpl.set('new_mail', row['new_mail'])
        tpl.set('new_report', row['new_report'])
        
        #---
        
        tpl.set('cur_planetid', self.currentPlanetId)
        tpl.set('cur_g', self.currentPlanetGalaxy)
        tpl.set('cur_s', self.currentPlanetSector)
        tpl.set('cur_p', ((self.currentPlanetId - 1) % 25) + 1)
        
        #---
        
        if self.profile['deletion_date']:
        
            tpl.set('delete_datetime', self.profile['deletion_date'])
            tpl.set('deleting')
        
        #---
        
        if self.profile['credits'] < 0:
        
            tpl.set('bankruptcy_hours', self.profile['credits_bankruptcy'])
            tpl.set('creditswarning')
        
        #---
                
        return Response(tpl.data)
