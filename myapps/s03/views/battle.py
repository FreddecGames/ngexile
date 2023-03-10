# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):

        battleId = ToInt(request.GET.get('id'), 0)
        if battleId == 0: return HttpResponseRedirect('/s03/reports/')
        
        fromview = ToInt(request.GET.get('v'), 0)
        if fromview == 0: return HttpResponseRedirect('/s03/reports/')
        
        #---
        
        result = dbExecute('SELECT battleid FROM battles_ships WHERE battleid=' + str(battleId) + ' AND owner_id=' + str(fromview) + ' LIMIT 1')
        display = result != None
        
        if not display and self.allianceId and self.allianceRights['can_see_reports']:
            result = dbExecute("SELECT owner_id FROM battles_ships WHERE battleid=" + str(battleId) + " AND (SELECT alliance_id FROM users WHERE id=owner_id)=" + str(self.allianceId) + " LIMIT 1")
            display = result != None
        
        if not display:
            key = request.GET.get("key", "")
            if key == "": return HttpResponseRedirect("/s03/reports/")
            result = dbExecute("SELECT 1 FROM battles WHERE id=" + str(battleId) + " AND key=" + dosql(key))
            display = result != None
            
        if not display: return HttpResponseRedirect("/s03/reports/")            
            
        #---
        
        content = getTemplate(request, 's03/battle')
    
        self.selectedMenu = 'reports'
        
        #---
        
        content.setValue('fromview', fromview)
        
        #---
        
        query = 'SELECT battles.id, time, planetid, name, galaxy, sector, planet, rounds, key' + \
                ' FROM battles' + \
                '  INNER JOIN nav_planet ON planetid=nav_planet.id' + \
                ' WHERE battles.id=' + str(battleId)
        battle = dbRow(query)
        content.setValue('battle', battle)
        
        #---
        
        query = 'SELECT fleet_id, shipid, destroyed_shipid, sum(count) AS count' + \
                ' FROM battles_fleets' + \
                '  INNER JOIN battles_fleets_ships_kills ON (battles_fleets.id=fleetid)' + \
                ' WHERE battleid=' + str(battleId) + \
                ' GROUP BY fleet_id, shipid, destroyed_shipid' + \
                ' ORDER BY sum(count) DESC'
        kills = dbRows(query)
        
        #---
        
        query = 'SELECT owner_name, fleet_name, shipid, shipcategory, shiplabel, count, lost, killed, won, relation1, owner_id , relation2, fleet_id, attacked, mod_shield, mod_handling, mod_tracking_speed, mod_damage, alliancetag' + \
                ' FROM sp_get_battle_result(' + str(battleId) + ',' + str(fromview) + ',' + str(fromview) + ')'
        battleShips = dbRows(query)
        
        fleets = []
        content.setValue('fleets', fleets)
        
        lastFleetId = -1
        lastCategory = -1
        
        for battleShip in battleShips:
        
            if battleShip['fleet_id'] != lastFleetId:
                lastFleetId = battleShip['fleet_id']
                
                fleet = { 'ships':[] }
                fleets.append(fleet)
                
                fleet['won'] = battleShip['won']
                fleet['name'] = battleShip['fleet_name']
                fleet['stance'] = battleShip['attacked']
                fleet['relation'] = battleShip['relation1']
                fleet['ownerName'] = battleShip['owner_name']
                fleet['allianceTag'] = battleShip['alliancetag']
            
                fleet['mod_shield'] = battleShip['mod_shield']
                fleet['mod_handling'] = battleShip['mod_handling']
                fleet['mod_tracking_speed'] = battleShip['mod_tracking_speed']
                fleet['mod_damage'] = battleShip['mod_damage']
            
            if battleShip['lost'] > 0 or battleShip['relation1'] >= 0: fleet['visible'] = True
            
            if not battleShip['won'] and battle['rounds'] <= 1 and battleShip['relation1'] < 0:
                
                if battleShip['shipcategory'] != lastCategory:
                    lastCategory = battleShip['shipcategory']
                    
                    ship = { 'category':battleShip['shipcategory'], 'count':0, 'lost':0, 'killed':0, 'after':0 }
                    fleet['ships'].append(ship)
                    
                ship['count'] += battleShip['count']
                ship['lost'] += battleShip['lost']
                ship['killed'] += battleShip['killed']
                ship['after'] += battleShip['count'] - battleShip['lost']
            
            else:
            
                ship = { 'kills':[] }
                fleet['ships'].append(ship)
                
                ship['name'] = battleShip['shiplabel']                
                ship['count'] = battleShip['count']
                ship['lost'] = battleShip['lost']
                ship['killed'] = battleShip['killed']
                ship['after'] = battleShip['count'] - battleShip['lost']
                
                for kill in kills:
                    if kill['fleet_id'] == battleShip['fleet_id'] and kill['shipid'] == battleShip['shipid']: 
                        ship['kills'].append({ 'name':getShipLabel(kill['destroyed_shipid']), 'count':kill['count'] })
                    
        #---
        
        content.setValue('baseurl', request.META.get('HTTP_HOST'))
        
        #---
        
        return self.display(content)
