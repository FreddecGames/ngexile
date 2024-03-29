# -*- coding: utf-8 -*-

from myapps.api.views._utils import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated ]
    
    
    def get(self, request, format=None):
        
        tpl = getTemplate()
        
        #---
        
        hours = 24 - timezone.now().hour

        query = 'SELECT scientists,soldiers,planets,ships_signature,ships_in_position_signature,ships_parked_signature,' + \
                ' cost_planets2,cost_scientists,cost_soldiers,cost_ships,cost_ships_in_position,cost_ships_parked,' + \
                ' int4(upkeep_scientists + scientists*cost_scientists/24*' + str(hours) + ') AS upkeep_scientists,' + \
                ' int4(upkeep_soldiers + soldiers*cost_soldiers/24*' + str(hours) + ') AS upkeep_soldiers,' + \
                ' int4(upkeep_planets + cost_planets2/24*' + str(hours) + ') AS upkeep_planets,' + \
                ' int4(upkeep_ships + ships_signature*cost_ships/24*' + str(hours) + ') AS upkeep_ships,' + \
                ' int4(upkeep_ships_in_position + ships_in_position_signature*cost_ships_in_position/24*' + str(hours) + ') AS upkeep_ships_in_position,' + \
                ' int4(upkeep_ships_parked + ships_parked_signature*cost_ships_parked/24*' + str(hours) + ') AS upkeep_ships_parked,' + \
                ' commanders, commanders_salary, cost_commanders, upkeep_commanders + int4(commanders_salary*cost_commanders/24*' + str(hours) + ') AS upkeep_commanders' + \
                ' FROM vw_players_upkeep' + \
                ' WHERE userid=' + str(self.userId)
        row = dbRow(query)

        tpl.set('upkeep', row)
        tpl.set('total_estimation', int(row['upkeep_scientists'] + row['upkeep_soldiers'] + row['upkeep_planets'] + row['upkeep_ships'] + row['upkeep_ships_in_position'] + row['upkeep_ships_parked'] + row['upkeep_commanders']))
        
        #---
        
        return Response(tpl.data)
