from .utils import *

class View(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        dbConnect()
        
        userId = int(request.session.get(sUser, 0))
        if not userId or userId == 0: return HttpResponseRedirect('/s03/')

        dbRow = dbRow('SELECT username FROM users WHERE id=' + str(userId))
        if dbRow['username']: return HttpResponseRedirect('/s03/')

        #--- post

        result = 0
        username = ''

        newName = request.POST.get('name', '')
        if newName != '':
            try:
                if isValidName(newName):
                    dbQuery('UPDATE users SET username=' + strSql(newName) + ' WHERE id=' + str(userId))
                    username = newName
                else:
                    result = 11
            except:
                result = 10

            if result == 0:
            
                galaxy = int(request.POST.get('galaxy', 0))
                dbRow = dbRow('SELECT sp_reset_account(' + str(userId) + ',' + str(galaxy) + ') AS result')

                if dbRow['result'] == 0:
                    
                    orientation = int(request.POST.get('orientation', 0))
                    dbQuery('UPDATE users SET orientation=' + str(orientation) + ' WHERE id=' + str(userId))

                    if orientation == 1:
                        dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 10, 1)')
                        dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 11, 1)')
                        dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 12, 1)')

                    elif orientation == 2:
                        dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 20, 1)')
                        dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 21, 1)')
                        dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 22, 1)')

                    elif orientation == 3:
                        dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 30, 1)')
                        dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 31, 1)')
                        dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 32, 1)')

                    dbQuery('SELECT sp_update_researches(' + str(userId) + ')')

                    return HttpResponseRedirect('/s03/empire-view/')

        #--- get
        
        content = getTemplateContext(self.request, 'home-start')
        
        content.assignValue('username', username)

        if result != 0: content.parse('error_' + str(result))

        list = []
        content.assignValue('galaxies', list)
        
        dbRows = dbRows('SELECT id, recommended FROM sp_get_galaxy_info(' + str(userId) + ')')
        for dbRow in dbRows:

            item = {}
            item['id'] = dbRow['id']
            item['recommendation'] = dbRow['recommended']

            list.append(item)

        return render(self.request, content.template, content.data)
