# -*- coding: utf-8 -*-

from myapps.api.views._utils import *

#---

class View(BaseView):

    def get(self, request, format=None):
        
        data = {}
        
        #---
        
        query = 'SELECT id, recommended' + \
                ' FROM sp_get_galaxy_info(' + str(self.userId) + ')'                
        rows = dbRows(query)
        
        data['galaxies'] = rows
        
        #---
        
        return Response(data)

    def post(self, request, format=None):
        
        data = {}

        #---
        
        action = request.data['action']

        #---
        
        if action == 'start':
                        
            name = ToStr(request.data['name'])
            if not isValidName(name):
                data['error'] = 'name_invalid'
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                dbQuery('UPDATE users SET username=' + dosql(name) + ' WHERE id=' + str(self.userId))
            except:
                data['error'] = 'name_already_used'
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
            orientation = ToInt(request.data.orientation, 0)
            if orientation == 0:
                data['error'] = 'orientation_invalid'
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            dbQuery('UPDATE users SET orientation=' + str(orientation) + ' WHERE id=' + str(self.userId))
            
            if orientation == 1:
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 10, 1)')
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 11, 1)')
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 12, 1)')

            elif orientation == 2:
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 20, 1)')
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 21, 1)')
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 22, 1)')

            elif orientation == 3:
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 30, 1)')
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 31, 1)')
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 32, 1)')

            dbQuery('SELECT sp_update_researches(' + str(self.userId) + ')')
            
            galaxy = ToInt(request.data.galaxy, 0)
            result = dbExecute('SELECT sp_reset_account(' + str(self.userId) + ',' + str(galaxy) + ')')
            if result != 0:
                data['error'] = 'reset_error_' + result
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(data)
            
        #---
        
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
