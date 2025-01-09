# -*- coding: utf-8 -*-

from myapps.s04.views._global import *

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

        if action == 'build':

            if self.current_planet['slot_count'] >= self.current_planet['slot_max']:
                messages.error(request, gettext('Pas assez de terrain pour ajouter le bâtiment.'))
                return HttpResponseRedirect(request.build_absolute_uri())

            id = request.POST.get('id')

            query = 'SELECT * FROM s04.vw_buildings' + \
                    ' WHERE planet_id=' + str(self.profile['planet_id']) + ' AND id=' + dosql(id)
            building = dbRow(query)

            if building['count'] >= building['max']:
                messages.error(request, gettext('Nombre maximal atteint pour le bâtiment.'))
                return HttpResponseRedirect(request.build_absolute_uri())

            query = 'SELECT * FROM s04.vw_building_building_reqs' + \
                    ' WHERE planet_id=' + str(self.profile['planet_id']) + ' AND building_id=' + dosql(id) + ' AND met = FALSE'
            reqs = dbRows(query)

            if len(reqs) > 0:
                messages.error(request, gettext('Exigences non staisfaites pour le bâtiment.'))
                return HttpResponseRedirect(request.build_absolute_uri())

            dbQuery('INSERT INTO s04.planet_buildings(planet_id, building_id, level) VALUES(' + str(self.profile['planet_id']) + ', ' + dosql(id) + ', 1)')

        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---
        
        tpl = getTemplate(request, 'planet-buildings')
        
        self.selectedTab = 'buildings'
        self.selectedMenu = 'planet'        
                
        #---

        query = 'SELECT * FROM s04.vw_buildings' + \
                ' WHERE planet_id=' + str(self.profile['planet_id'])
        rows = dbRows(query)

        buildings = []
        tpl.set('buildings', buildings)

        for row in rows:

            building = row

            query = 'SELECT * FROM s04.vw_building_building_reqs' + \
                    ' WHERE planet_id=' + str(self.profile['planet_id']) + ' AND building_id=' + dosql(row['id'])
            building['reqs'] = dbRows(query)

            building['can_build'] = True
            if self.current_planet['slot_count'] >= self.current_planet['slot_max']: building['can_build'] = False
            elif building['count'] >= building['max']: building['can_build'] = False

            buildings.append(building)

        #---

        query = 'SELECT * FROM s04.vw_planet_buildings' + \
                ' WHERE planet_id=' + str(self.profile['planet_id'])
        rows = dbRows(query)

        categories = []
        tpl.set('categories', categories)

        lastCategory = -1
        
        for row in rows:

            if row['category'] != lastCategory:
                lastCategory = row['category']
                
                category = { 'id':row['category'], 'buildings':[] }
                categories.append(category)
        
            category['buildings'].append(row)

        #---
        
        return self.display(tpl, request)
