# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GameView):
    
    ################################################################################
    
    def dispatch(self, request, galaxy, sector):

        #---

        response = super().pre_dispatch(request)
        if response: return response
        
        #---
        
        return super().dispatch(request)
        
    ################################################################################
    
    def get(self, request, galaxy, sector):
        
        #---
        
        if galaxy == '':

            #---
            
            tpl = Template('map-universe')

            self.selectedTab = 'universe'
            self.selectedMenu = 'map'        
        
            #---
            
            galaxies = dbRows('SELECT * FROM vw_galaxies')        
            tpl.set('galaxies', galaxies)
                            
            #---
            
            return self.display(request, tpl)

        #---

        elif sector == '':

            #---
            
            tpl = Template('map-galaxy')

            self.selectedTab = 'galaxy'
            self.selectedMenu = 'map'        
            
            #---
            
            galaxy = dbRows('SELECT * FROM vw_galaxies WHERE id=' + str(galaxy))        
            tpl.set('galaxy', galaxy)
            
            #---
            
            planets = dbRows('SELECT * FROM vw_planets WHERE galaxy_id=' + str(galaxy))        
            tpl.set('planets', planets)
            
            #---

            return self.display(request, tpl)

        #---

        else:
        
            #---
            
            tpl = Template('map-sector')

            self.selectedTab = 'sector'
            self.selectedMenu = 'map'
            
            self.showHeader = True
            self.headerUrl = '/ng0/map/'
            
            #---
            
            tpl.set('galaxy', galaxy)
            tpl.set('sector', sector)
            
            #---
        
            tpl.set('sector0', self.getSector(sector,-1,-1))
            tpl.set('sector1', self.getSector(sector, 0,-1))
            tpl.set('sector2', self.getSector(sector, 1,-1))
            tpl.set('sector3', self.getSector(sector, 1, 0))
            tpl.set('sector4', self.getSector(sector, 1, 1))
            tpl.set('sector5', self.getSector(sector, 0, 1))
            tpl.set('sector6', self.getSector(sector,-1, 1))
            tpl.set('sector7', self.getSector(sector,-1, 0))

            #---

            sectorRadar = dbExecute('SELECT * FROM profile_sector_radar(' + str(self.userId) + ',' + str(galaxy) + ',' + str(sector) + ')')
            tpl.set('sectorRadar', sectorRadar)
            
            #---
            
            planets = dbRows('SELECT * FROM vw_planets WHERE galaxy_id=' + str(galaxy) + ' AND sector=' + str(sector))        
            tpl.set('planets', planets)
            
            for planet in planets:
            
                planet['fleets'] = dbRows('SELECT * FROM ng0.vw_fleets WHERE planet_id=' + str(planet['id']))

            #---
            
            if sectorRadar > 0:
                
                movings = dbRows('SELECT * FROM vw_fleets WHERE action=\'move\' AND ((origin_galaxy=' + str(galaxy) + ' AND origin_sector=' + str(sector) + ') OR (dest_galaxy=' + str(galaxy) + ' AND dest_sector=' + str(sector) + '))')
                tpl.set('movings', movings)
                
            #---
            
            return self.display(request, tpl)

    ################################################################################
    
    def getSector(self, sector, shiftX, shiftY):

        if (sector % 10 == 0) and (shiftX > 0): shiftX = 0
        if (sector % 10 == 1) and (shiftX < 0): shiftX = 0

        if (sector < 11) and (shiftY < 0): shiftY = 0
        if (sector > 90) and (shiftY > 0): shiftY = 0

        s = sector + shiftX + shiftY * 10

        if s > 100: s = 100

        return s
