from .utils import *

class View(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        dbConnect()
        
        userId = int(request.session.get(sUser, 0))
        if not userId or userId == 0: return HttpResponseRedirect('/s03/')

        dbRow = dbRow('SELECT int4(count(1)) FROM nav_planet WHERE ownerid=' + str(userId))
        planets = dbRow['count']

        dbRow = dbRow('SELECT username, resets, credits_bankruptcy, int4(score_research) FROM users WHERE id=' + str(userId))
        username = dbRow['username']
        resets = dbRow['resets']
        bankruptcy = dbRow['credits_bankruptcy']
        research_done = dbRow['score_research']

        if planets > 0 and bankruptcy > 0: return HttpResponseRedirect('/s03/')

        if resets == 0: return HttpResponseRedirect('/s03/home-start/')
        
        #--- post

        resetError = 0
        changeNameError = ''
        
        action = request.POST.get('action', '')

        if action == 'retry':
        
            if request.POST.get('username') != username:
            
                if not isValidName(request.POST.get('username')):
                    changeNameError = 'check_username'
                    
                else:
                    dbQuery('UPDATE users SET alliance_id=NULL WHERE id=' + str(userId))
                    dbQuery('UPDATE users SET username=' + strSql(request.POST.get('username')) + ' WHERE id=' + str(userId))
                    dbQuery('UPDATE commanders SET name=' + strSql(request.POST.get('username')) + ' WHERE name=' + strSql(username) + ' AND ownerid=' + str(userId))
                    
            if changeNameError == '':
                dbRow = dbRow('SELECT sp_reset_account(' + str(userId) + ',' + str(toInt(request.POST.get('galaxy'), 1)) + ') AS result')
                if dbRow['result'] == 0: return HttpResponseRedirect('/s03/empire-view/')
                else: resetError = dbRow['result']

        elif action == 'abandon':
            dbQuery('UPDATE users SET deletion_date=now() WHERE id=' + str(userId))
            return HttpResponseRedirect('/s03/')

        #--- get
        
        content = getTemplateContext(self.request, 'home-gameover')
        content.assignValue('username', username)

        if changeNameError != '': action = 'continue'

        if action == 'continue':

            list = []
            content.assignValue('galaxies', list)
            
            dbRows = dbRows('SELECT id, recommended FROM sp_get_galaxy_info(' + str(userId) + ')')
            for dbRow in dbRows:
                
                item = {}
                item['id'] = dbRow['id']
                item['recommendation'] = dbRow['recommended']
                
                list.append(item)

            if changeNameError != '':
                content.parse(changeNameError)
                content.parse('error')

            content.parse('changename')
            
        else:
        
            content.parse('retry')

            if bankruptcy > 0: content.parse('gameover')
            else: content.parse('bankrupt')

        if resetError != 0:
        
            if resetError == 4:
                content.parse('no_free_planet')
                
            else:
                content.assignValue('userid', userId)
                content.assignValue('resetError', resetError)
                content.parse('resetError')

        return render(self.request, content.template, content.data)
