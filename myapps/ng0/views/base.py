from .utils import *

class BaseView(LoginRequiredMixin, View):
    
    profile = None
    selectedMenu = None
    currentPlanet = None
    showPlanetHeader = False
    
    def pre_dispatch(self, request, *args, **kwargs):
        
        dbConnect()
        
        # check profile
        
        query = 'SELECT users.id, username, privilege, users.credits, lastplanetid, deletion_date, alliance_id, alliances.tag AS alliance_tag, alliances.name AS alliance_name,' + \
                ' credits_bankruptcy, prestige_points AS prestiges, users.score, users.avatar_url,' + \
                ' (SELECT int4(COUNT(*)) FROM messages WHERE ownerid = users.id AND read_date is NULL) AS unread_mails,' + \
                ' (SELECT int4(COUNT(*)) FROM reports WHERE ownerid = users.id AND read_date is NULL AND datetime <= now()) AS unread_reports' + \
                ' FROM users' + \
                '  LEFT JOIN alliances ON alliances.id = users.alliance_id' + \
                ' WHERE users.id=' + str(request.user.id)
        self.profile = dbRow(query)        
        if self.profile == None: return HttpResponseRedirect('/ng0/')

        if self.profile['privilege'] == -1: return HttpResponseRedirect('/ng0/home-locked/')
        if self.profile['privilege'] == -2: return HttpResponseRedirect('/ng0/home-holidays/')
        if self.profile['privilege'] == -3: return HttpResponseRedirect('/ng0/home-wait/')
        
        if self.profile['credits_bankruptcy'] <= 0: return HttpResponseRedirect('/ng0/home-gameover/')
        
        # log activity
        
        if not self.request.user.is_impersonate:
            dbQuery('SELECT sp_log_activity(' + str(self.profile['id']) + ',' + strSql(self.request.META.get('REMOTE_ADDR')) + ', 0)')
        
        # set current planet
        
        planetId = toInt(self.request.GET.get('planetId'), 0)
        
        if planetId != 0:

            self.currentPlanet = dbRow('SELECT id, galaxy, sector, planet AS number, name, planet_floor AS floor FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND id=' + str(planetId) + ' and ownerid=' + str(self.profile['id']))

            if not self.request.user.is_impersonate:
                dbQuery('UPDATE users SET lastplanetid=' + str(planetId) + ' WHERE id=' + str(self.profile['id']))

            return HttpResponseRedirect('/s03/empire-view/')
        
        if self.currentPlanet == None:

            self.currentPlanet = dbRow('SELECT id, galaxy, sector, planet AS number, name, planet_floor AS floor FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND id=' + str(self.profile['lastplanetid']) + ' and ownerid=' + str(self.profile['id']))
            print(self.currentPlanet)
            
            return
    
        self.currentPlanet = oConnExecute('SELECT id, galaxy, sector, planet AS number, name, planet_floor AS floor FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=' + str(self.profile['id']) + ' LIMIT 1')
        if self.currentPlanet == None: return HttpResponseRedirect('/ng0/home-gameover/')
    
        if not self.request.user.is_impersonate:
            dbQuery('UPDATE users SET lastplanetid=' + str(planetId) + ' WHERE id=' + str(self.profile['id']))

        return HttpResponseRedirect('/s03/empire-view/')

    def display(self, tpl):
        
        if self.request.user.is_impersonate:
            self.profile['is_impersonating'] = True
        
        query = 'SELECT int4(count(1)) AS players, (SELECT int4(count(1)) FROM vw_players WHERE score >= ' + str(self.profile['score']) + ') AS ranking FROM vw_players'
        result = dbRow(query)
        self.profile = self.profile | result
        
        tpl.assignValue('profile', self.profile)
        tpl.assignValue('selectedMenu', self.selectedMenu)
        
        self.currentPlanet['img'] = getPlanetImg(self.currentPlanet['id'], self.currentPlanet['floor'])
        
        tpl.assignValue('currentPlanet', self.currentPlanet)    
        
        if self.showPlanetHeader == True: self.displayPlanetHeader(tpl)
        
        return render(self.request, tpl.template, tpl.data)

    def displayPlanetHeader(self, tpl):
    
        # current planet
        
        query = 'SELECT ore, ore_production, ore_capacity, mod_production_ore,' + \
                ' hydrocarbon, hydrocarbon_production, hydrocarbon_capacity, mod_production_hydrocarbon,' + \
                ' energy, energy_consumption, energy_production, energy_capacity,' + \
                ' floor_occupied, floor,' + \
                ' space_occupied, space, ' + \
                ' workers, workers_busy, workers_for_maintenance, workers_capacity,' + \
                ' soldiers, soldiers_capacity,' + \
                ' scientists, scientists_capacity' + \
                ' FROM vw_planets WHERE id=' + str(self.currentPlanet['id'])
        dbRow = dbRow(query)
        
        dbRow['energy_production'] = dbRow['energy_production'] - dbRow['energy_consumption']
        
        dbRow['ore_level'] = getPercent(dbRow['ore'], dbRow['ore_capacity'], 10)
        dbRow['hydrocarbon_level'] = getPercent(dbRow['hydrocarbon'], dbRow['hydrocarbon_capacity'], 10)
        
        dbRow['workers_idle'] = dbRow['workers'] - dbRow['workers_busy']
        
        if dbRow['soldiers'] * 250 < dbRow['workers'] + dbRow['scientists']: dbRow['soldiers_low'] = True

        if dbRow['mod_production_ore'] < 0 or dbRow['workers'] < dbRow['workers_for_maintenance']: dbRow['ore_production_anormal'] = True
        if dbRow['mod_production_hydrocarbon'] < 0 or dbRow['workers'] < dbRow['workers_for_maintenance']: dbRow['hydrocarbon_production_anormal'] = True

        tpl.assignValue('planetHeader', dbRow)
        
        # special buildings on current planet
        
        query = 'SELECT buildingid' + \
                ' FROM planet_buildings INNER JOIN db_buildings ON (db_buildings.id=buildingid AND db_buildings.is_planet_element)' + \
                ' WHERE planetid=' + str(self.currentPlanet['id']) + \
                ' ORDER BY upper(db_buildings.label)'
        dbRows = oConnExecuteAll(query)        
        
        # user planets
                
        query = 'SELECT id, name, galaxy, sector, planet' + \
                ' FROM nav_planet' + \
                ' WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=' + str(self.profile['id']) + \
                ' ORDER BY id'
        dbRows = dbRows(query)

        planets = []    
        tpl.assignValue('planets', planets)
        
        for dbRow in dbRows:
    
            planet = dbRow
            planets.append(planet)
                
            if dbRow['id'] == self.currentPlanet['id']: dbRow['selected'] = True
