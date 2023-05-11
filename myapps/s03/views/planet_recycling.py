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
        
        if action == 'recycle':
        
            rows = dbRows('SELECT id FROM db_ships')
            for row in rows:
            
                quantity = ToInt(request.POST.get('s' + str(row['id'])), 0)
                if quantity > 0:
                    dbQuery('SELECT sp_start_ship_recycling(' + str(self.currentPlanetId) + ',' + str(row['id']) + ',' + str(quantity) + ')')
        
        #---
        
        elif action == 'cancel':
        
            queueId = ToInt(request.POST.get('q'), 0)
            if queueId != 0:            
                dbQuery('SELECT sp_cancel_ship(' + str(self.currentPlanetId) + ', ' + str(queueId) + ')')                
                
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    ################################################################################
    
    def get(self, request, *args, **kwargs):
    
        #---
        
        tpl = getTemplate(request, 'planet-recycling')
        
        self.selectedMenu = 'planet'
        
        self.headerUrl = '/s03/planet-recycling/'
        self.showHeader = True
        
        #---
        
        query = 'SELECT v.id, v.category, v.label, v.description, int4(v.cost_ore * const_recycle_ore(planet_ownerid)) AS cost_ore, int4(v.cost_hydrocarbon * const_recycle_hydrocarbon(planet_ownerid)) AS cost_hydrocarbon, v.cost_credits, v.workers, v.crew, v.capacity,' + \
                ' int4(const_ship_recycling_multiplier() * v.construction_time) as construction_time, v.hull, v.shield, v.weapon_power, v.weapon_ammo, v.weapon_tracking_speed, v.weapon_turrets, v.signature, v.speed,' + \
                ' v.handling, v.buildingid, v.recycler_output, v.droppods, v.long_distance_capacity, v.quantity, true, true,' + \
                ' NULL, 0, COALESCE(v.new_shipid, v.id) AS shipid' + \
                ' FROM vw_ships AS v' + \
                '   INNER JOIN db_ships AS db ON db.id = v.id' + \
                '   LEFT JOIN db_ships AS r ON r.id = v.required_shipid' + \
                ' WHERE quantity > 0 AND planetid=' + str(self.currentPlanetId)
        rows = dbRows(query)
        
        categories = []
        tpl.set('categories', categories)
        
        lastCategory = -1        
        for row in rows:
            
            catId = row['category']
            if catId != lastCategory:
                lastCategory = catId
            
                category = { 'id':catId, 'ships':[] }
                categories.append(category)

            category['ships'].append(row)
            
        #---
        
        query = 'SELECT s.id, shipid, remaining_time, quantity, end_time, recycle, s.required_shipid, int4(s.cost_ore*const_recycle_ore(ownerid)) AS r_cost_ore, int4(s.cost_hydrocarbon*const_recycle_hydrocarbon(ownerid)) AS r_cost_hydrocarbon, s.cost_ore, s.cost_hydrocarbon, s.cost_energy, s.crew,' + \
                ' db_ships.label, r.label AS r_label' + \
                ' FROM vw_ships_under_construction AS s' + \
                '   INNER JOIN db_ships ON db_ships.id = shipid' + \
                '   LEFT JOIN db_ships AS r ON r.id = s.required_shipid' + \
                ' WHERE planetid=' + str(self.currentPlanetId) + \
                ' ORDER BY start_time, shipid'
        rows = dbRows(query)

        queues = []
        tpl.set('queues', queues)
        
        underconstructions = []
        tpl.set('underconstructions', underconstructions)
        
        for row in rows:
        
            if row['end_time']: underconstructions.append(row)
            else: queues.append(row)
        
        #---
        
        return self.display(tpl, request)
