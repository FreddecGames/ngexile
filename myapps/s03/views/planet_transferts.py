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
        
        if action == 'cancel':
        
            energy_to = ToInt(request.POST.get('to'), 0)
            energy_from = ToInt(request.POST.get('from'), 0)

            if energy_from != 0: query = 'DELETE FROM planet_energy_transfer WHERE planetid=' + str(energy_from) + ' AND target_planetid=' + str(self.currentPlanetId)
            else: query = 'DELETE FROM planet_energy_transfer WHERE planetid=' + str(self.currentPlanetId) + ' AND target_planetid=' + str(energy_to)
            dbQuery(query)
        
        #---
        
        elif action == 'submit':
            
            update_planet = False
            
            query = 'SELECT target_planetid, energy, enabled' + \
                    ' FROM planet_energy_transfer' + \
                    ' WHERE planetid=' + str(self.currentPlanetId)
            rows = dbRows(query)

            for row in rows:
                
                query = ''

                energy = ToInt(request.POST.get('energy_' + str(row['target_planetid'])), 0)
                if energy != row['energy']: query = query + 'energy = ' + str(energy)

                enabled = request.POST.get('enabled_' + str(row['target_planetid']))
                if enabled == '1': enabled = True
                else: enabled = False

                if enabled != row['enabled']:
                    if query != '': query = query + ','
                    query = query + 'enabled=' + str(enabled)

                if query != '':
                
                    query = 'UPDATE planet_energy_transfer SET ' + query + ' WHERE planetid=' + str(self.currentPlanetId) + ' AND target_planetid=' + str(row['target_planetid'])
                    dbQuery(query)

                    update_planet = True

            g = ToInt(request.POST.get('to_g'), 0)
            s = ToInt(request.POST.get('to_s'), 0)
            p = ToInt(request.POST.get('to_p'), 0)
            energy = ToInt(request.POST.get('energy'), 0)

            if g != 0 and s != 0 and p != 0 and energy > 0:
            
                query = 'INSERT INTO planet_energy_transfer(planetid, target_planetid, energy) VALUES(' + str(self.currentPlanetId) + ', sp_planet(' + str(g) + ',' + str(s) + ',' + str(p) + '),' + str(energy) + ')'
                dbQuery(query)

                update_planet = True

            if update_planet:
            
                query = 'SELECT sp_update_planet(' + str(self.currentPlanetId) + ')'
                dbQuery(query)
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
    
    ################################################################################
    
    def get(self, request, *args, **kwargs):

        #---

        tpl = getTemplate(request, 'planet-transferts')
        
        self.selectedTab = 'transferts'
        self.selectedMenu = 'planet'

        self.showHeader = True
        self.headerUrl = '/s03/planet-transferts/'
        
        #---
        
        query = 'SELECT energy_receive_antennas, energy_send_antennas FROM nav_planet WHERE id=' + str(self.currentPlanetId)
        planet = dbRow(query)
        
        tpl.set('planet', planet)
        
        max_receive = planet['energy_receive_antennas']
        max_send = planet['energy_send_antennas']
        
        #---
        
        query = 'SELECT t.planetid, sp_get_planet_name(' + str(self.userId) + ', n1.id) AS planetname, sp_relation(n1.ownerid,' + str(self.userId) + ') AS relation, n1.galaxy, n1.sector, n1.planet, ' + \
                '        t.target_planetid, sp_get_planet_name(' + str(self.userId) + ', n2.id) AS target_planetname, sp_relation(n2.ownerid,' + str(self.userId) + ') AS target_relation, n2.galaxy AS target_galaxy, n2.sector AS target_sector, n2.planet AS target_planet, ' + \
                '        t.energy, t.effective_energy, enabled' + \
                ' FROM planet_energy_transfer t' + \
                '    INNER JOIN nav_planet n1 ON (t.planetid=n1.id)' + \
                '    INNER JOIN nav_planet n2 ON (t.target_planetid=n2.id)' + \
                ' WHERE planetid=' + str(self.currentPlanetId) + ' OR target_planetid=' + str(self.currentPlanetId) + \
                ' ORDER BY not enabled, planetid, target_planetid'
        rows = dbRows(query)

        receiving = 0
        sending_enabled = 0

        sents = []
        tpl.set('sents', sents)
        
        receiveds = []
        tpl.set('receiveds', receiveds)
        
        for row in rows:
        
            item = {}
            
            item['energy'] = row['energy']
            item['effective_energy'] = row['effective_energy']
            
            item['loss'] = getPercent(row['energy'] - row['effective_energy'], row['energy'], 1)

            if row['planetid'] == self.currentPlanetId:
            
                if row['enabled']:
                    sending_enabled = sending_enabled + 1
                    item['enabled'] = True
                    
                item['planetid'] = row['target_planetid']
                item['name'] = row['target_planetname']
                item['rel'] = row['target_relation']
                item['g'] = row['target_galaxy']
                item['s'] = row['target_sector']
                item['p'] = row['target_planet']

                sents.append(item)
                
            elif row['enabled']:

                receiving = receiving + 1

                item['planetid'] = row['planetid']
                item['name'] = row['planetname']
                item['rel'] = row['relation']
                item['g'] = row['galaxy']
                item['s'] = row['sector']
                item['p'] = row['planet']

                receiveds.append(item)

        tpl.set('antennas_receive_used', receiving)
        tpl.set('antennas_send_used', sending_enabled)

        if max_send == 0: tpl.set('send_no_antenna')
        if max_receive == 0: tpl.set('receive_no_antenna')

        if receiving > 0:
            tpl.set('cant_send_when_receiving')
            max_send = 0

        if sending_enabled > 0:
            tpl.set('cant_receive_when_sending')
            max_receive = 0
        elif receiving == 0 and max_receive > 0:
            tpl.set('receiving_none')

        if max_receive > 0: tpl.set('receive')
        if max_send - len(sents) > 0: tpl.set('send')
        if max_send > 0: tpl.set('submit')
        
        #---

        return self.display(tpl, request)
