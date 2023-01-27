from myapps.ng0.views.base import *

from myapps.ng0.engine.battle import *

ships = {

    'fighter': { 'id':'fighter', 'hull':350, 'shield':0, 'handling':1400, 'tracking':2200, 'turrets':1, 'damages':{ 'em':0, 'explosive':0, 'kinetic':0, 'thermal':20 }, 'resistances':{ 'em':0, 'explosive':85, 'kinetic':0, 'thermal':30 } },
    'cruiser': { 'id':'cruiser', 'hull':10000, 'shield':20000, 'handling':400, 'tracking':720, 'turrets':4, 'damages':{ 'em':0, 'explosive':0, 'kinetic':400, 'thermal':0 }, 'resistances':{ 'em':30, 'explosive':65, 'kinetic':45, 'thermal':85 } },
}

class View(BaseView):
    
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        
        battle = CBattle()
        
        battle.addShipGroup(1, 0, ships['fighter']['id'], ships['fighter']['hull'], ships['fighter']['shield'], ships['fighter']['handling'], ships['fighter']['tracking'], ships['fighter']['turrets'], ships['fighter']['damages'], ships['fighter']['resistances'], 495)
        battle.addShipGroup(2, 0, ships['cruiser']['id'], ships['cruiser']['hull'], ships['cruiser']['shield'], ships['cruiser']['handling'], ships['cruiser']['tracking'], ships['cruiser']['turrets'], ships['cruiser']['damages'], ships['cruiser']['resistances'], 1)
        
        rounds = 0
        battle.beginFight()
        while rounds < 25 and battle.doRound():
            rounds = rounds + 1
        
        content = getTemplate(self.request, 'report_battle')
        
        content.setValue('rounds', rounds)
        content.setValue('shipGroups', battle.shipGroupList)
        
        return self.display(content)
        