from .utils import *

class View(BaseMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        userId = int(request.session.get(sUser, 0))
        if not userId or userId == 0: return HttpResponseRedirect('/s03/')

        result = oConnExecute('SELECT int4(count(1)) FROM nav_planet WHERE ownerid=' + str(userId))
        planets = result[0]

        result = oConnExecute('SELECT username, resets, credits_bankruptcy, int4(score_research) FROM users WHERE id=' + str(userId))
        username = oRs[0]
        resets = oRs[1]
        bankruptcy = oRs[2]
        research_done = oRs[3]

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
                    oConnDoQuery('UPDATE users SET alliance_id=NULL WHERE id=' + str(userId))
                    oConnDoQuery('UPDATE users SET username=' + dosql(request.POST.get('username')) + ' WHERE id=' + str(userId))
                    oConnDoQuery('UPDATE commanders SET name=' + dosql(request.POST.get('username')) + ' WHERE name=' + dosql(username) + ' AND ownerid=' + str(userId))
                    
            if changeNameError == '':
                oRs = oConnExecute('SELECT sp_reset_account(' + str(userId) + ',' + str(ToInt(request.POST.get('galaxy'), 1)) + ')')
                if oRs[0] == 0: return HttpResponseRedirect('/s03/empire-view/')
                else: resetError = oRs[0]

        elif action == 'abandon':
            oConnDoQuery('UPDATE users SET deletion_date=now() WHERE id=' + str(userId))
            return HttpResponseRedirect('/s03/')

        #--- get
        
        content = GetTemplate(self.request, 'home-gameover')
        content.AssignValue('username', username)

        if changeNameError != '': action = 'continue'

        if action == 'continue':

            list = []
            content.AssignValue('galaxies', list)
            
            oRss = oConnExecuteAll('SELECT id, recommended FROM sp_get_galaxy_info(' + str(userId) + ')')
            for oRs in oRss:
                
                item = {}
                item['id'] = oRs[0]
                item['recommendation'] = oRs[1]
                
                list.append(item)

            if changeNameError != '':
                content.Parse(changeNameError)
                content.Parse('error')

            content.Parse('changename')
            
        else:
        
            content.Parse('retry')

            if bankruptcy > 0: content.Parse('gameover')
            else: content.Parse('bankrupt')

        if resetError != 0:
        
            if resetError == 4:
                content.Parse('no_free_planet')
                
            else:
                content.AssignValue('userid', userId)
                content.AssignValue('resetError', resetError)
                content.Parse('resetError')

        return render(self.request, content.template, content.data)
