from .base import *

class View(BaseView):
    
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- get
        
        content = getTemplateContext(request, 'empire-view')
        
        self.selectedMenu = 'empire'
        
        # alliance data
        
        if self.profile['alliance_id']:
        
            query = 'SELECT announce, tag, name, defcon FROM alliances WHERE id=' + str(self.profile['alliance_id'])
            alliance = dbRow(query)
            content.assignValue('alliance', alliance)
        
        # stats data
        
        query = 'SELECT orientation, score, previous_score, mod_planets::integer, mod_commanders::integer FROM users WHERE id=' + str(self.profile['id'])
        stats = dbRow(query)
        
        stats['score_delta'] = stats['score'] - stats['previous_score']
        
        query = 'SELECT int4(count(1)) AS commanders FROM commanders WHERE recruited IS NOT NULL AND ownerid=' + str(self.profile['id'])
        result = dbRow(query)
        stats = stats | result
        
        query = 'SELECT int4(count(1)) AS players, (SELECT int4(count(1)) FROM vw_players WHERE score >= ' + str(stats['score']) + ') AS ranking FROM vw_players'
        result = dbRow(query)
        stats = stats | result
        
        query = 'SELECT count(1) AS planets,' + \
                ' sum(ore_production) AS ore_prod, sum(hydrocarbon_production) AS hydro_prod,' + \
                ' int4(sum(workers)) AS workers, int4(sum(scientists)) AS scientists, int4(sum(soldiers)) AS soldiers' + \
                ' FROM vw_planets WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=' + str(self.profile['id'])
        result = dbRow(query)
        stats = stats | result
        
        query = 'SELECT int4(sum(cargo_workers)) AS workers, int4(sum(cargo_scientists)) AS scientists, int4(sum(cargo_soldiers)) AS soldiers' + \
                ' FROM fleets WHERE ownerid=' + str(self.profile['id'])
        result = dbRow(query)
        stats['workers'] += result['workers']
        stats['scientists'] += result['scientists']
        stats['soldiers'] += result['soldiers']
        
        content.assignValue('stats', stats)
        
        # movings data
        
        query = 'SELECT fleets.id, fleets.name, fleets.owner_name, fleets.signature, fleets.attackonsight AS stance,' + \
                ' COALESCE(((SELECT vw_relations.relation FROM vw_relations WHERE vw_relations.user1=' + str(self.profile['id']) + ' AND vw_relations.user2 = fleets.ownerid)), -3) AS relation,' + \
                ' fleets.destplanetid, fleets.destplanet_name, COALESCE(((SELECT vw_relations.relation FROM vw_relations WHERE vw_relations.user1=' + str(self.profile['id']) + ' AND vw_relations.user2 = fleets.destplanet_ownerid)), -3) AS destplanet_relation, fleets.destplanet_galaxy, fleets.destplanet_sector, fleets.destplanet_planet,' + \
                ' COALESCE(fleets.remaining_time, 0) AS remaining_time' + \
                ' FROM vw_fleets AS fleets ' + \
                ' WHERE fleets.ownerid != ' + str(self.profile['id']) + ' AND (action = 1 OR action = -1) AND ((destplanetid IS NOT NULL AND destplanetid IN (SELECT id FROM nav_planet WHERE ownerid=' + str(self.profile['id']) + ')))' + \
                ' ORDER BY COALESCE(remaining_time, 0), ownerid'
        results = dbRows(query)
        movings = results
        
        content.assignValue('movings', movings)
        
        # upkeep data
        
        hours = 24 - timezone.now().hour

        query = 'SELECT int4(upkeep_ships + ships_signature * cost_ships / 24 *' + str(hours) + ') AS ships,' + \
                ' int4(upkeep_ships_in_position + ships_in_position_signature * cost_ships_in_position / 24 *' + str(hours) + ') AS inposition,' + \
                ' int4(upkeep_ships_parked + ships_parked_signature * cost_ships_parked / 24 *' + str(hours) + ') As parked,' + \
                ' int4(upkeep_commanders + commanders_salary * cost_commanders / 24 *' + str(hours) + ') AS commanders,' + \
                ' int4(upkeep_planets + cost_planets2 / 24 *' + str(hours) + ') AS planets,' + \
                ' int4(upkeep_scientists + scientists * cost_scientists / 24 *' + str(hours) + ') AS scientists,' + \
                ' int4(upkeep_soldiers + soldiers * cost_soldiers / 24 *' + str(hours) + ') AS soldiers' + \
                ' FROM vw_players_upkeep' + \
                ' WHERE userid=' + str(self.profile['id'])
        result = dbRow(query)
        upkeep = result
        
        upkeep['total'] = upkeep['ships'] + upkeep['inposition'] + upkeep['parked'] + upkeep['commanders'] + upkeep['planets'] + upkeep['scientists'] + upkeep['soldiers']
        
        content.assignValue('upkeep', upkeep)

        # tech data
        
        query = 'SELECT researchid, int4(date_part(\'epoch\', end_time - now())) AS remaining_time, db_research.label' + \
                ' FROM researches_pending' + \
                '   LEFT JOIN db_research ON researchid=db_research.id' + \
                ' WHERE userid=' + str(self.profile['id'])
        result = dbRow(query)
        tech = result
        
        content.assignValue('tech', tech)
        
        return self.display(content)
