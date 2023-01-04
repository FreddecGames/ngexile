from .utils import *

class View(BaseMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        userId = int(request.session.get(sUser, 0))
        if not userId or userId == 0: return HttpResponseRedirect('/s03/')

        result = oConnExecute('SELECT username FROM users WHERE id=' + str(userId))
        if not result: return HttpResponseRedirect('/s03/')
        username = result[0]

        #--- post

        result = 0

        newName = request.POST.get('name', '')
        if newName != '':
            try:
                if isValidName(newName):
                    oConnDoQuery('UPDATE users SET username=' + dosql(newName) + ' WHERE id=' + str(userId))
                    username = newName
                else:
                    result = 11
            except:
                result = 10

            if result == 0:
            
                galaxy = int(request.POST.get('galaxy', 0))
                result = oConnExecute('SELECT sp_reset_account(' + str(userId) + ',' + str(galaxy) + ')')

                if result[0] == 0:
                    
                    orientation = int(request.POST.get('orientation', 0))
                    oConnDoQuery('UPDATE users SET orientation=' + str(orientation) + ' WHERE id=' + str(userId))

                    if orientation == 1:
                        oConnDoQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 10, 1)')
                        oConnDoQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 11, 1)')
                        oConnDoQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 12, 1)')

                    elif orientation == 2:
                        oConnDoQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 20, 1)')
                        oConnDoQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 21, 1)')
                        oConnDoQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 22, 1)')

                    elif orientation == 3:
                        oConnDoQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 30, 1)')
                        oConnDoQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 31, 1)')
                        oConnDoQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(userId) + ', 32, 1)')

                    oConnExecute('SELECT sp_update_researches(' + str(userId) + ')')

                    return HttpResponseRedirect('/s03/empire-view/')

        #--- get
        
        content = GetTemplate(self.request, 'home-start')
        
        content.AssignValue('username', username)

        if result != 0: content.Parse('error_' + str(result))

        list = []
        content.AssignValue('galaxies', list)
        
        results = oConnExecuteAll('SELECT id, recommended FROM sp_get_galaxy_info(' + str(userId) + ')')
        for result in results:

            item = {}
            item['id'] = result[0]
            item['recommendation'] = result[1]

            list.append(item)

        return render(self.request, content.template, content.data)
