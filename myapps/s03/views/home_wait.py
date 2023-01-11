from .utils import *

class View(BaseMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        userId = int(request.session.get(sUser, 0))
        if not userId or userId == 0: return HttpResponseRedirect('/s03/')

        dbRow = oConnRow('SELECT username FROM users WHERE privilege=-3 AND id=' + str(userId))
        if not dbRow['username']: return HttpResponseRedirect('/s03/')
        
        #--- post
        
        action = request.POST.get('unlock', '')
        if action != '':
        
            oConnDoQuery('UPDATE users SET privilege=0 WHERE id=' + str(userId))
            return HttpResponseRedirect('/s03/')
        
        #--- get
        
        content = GetTemplate(self.request, 'home-wait')
        
        username = dbRow['username']
        content.AssignValue('username', username)

        return render(self.request, content.template, content.data)
