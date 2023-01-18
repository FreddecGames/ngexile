from .utils import *

class View(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        dbConnect()
        
        userId = int(request.session.get(sUser, 0))
        if not userId or userId == 0: return HttpResponseRedirect('/s03/')

        dbRow = dbRow('SELECT username FROM users WHERE privilege=-3 AND id=' + str(userId))
        if not dbRow['username']: return HttpResponseRedirect('/s03/')
        
        #--- post
        
        action = request.POST.get('unlock', '')
        if action != '':
        
            dbQuery('UPDATE users SET privilege=0 WHERE id=' + str(userId))
            return HttpResponseRedirect('/s03/')
        
        #--- get
        
        content = getTemplateContext(self.request, 'home-wait')
        
        username = dbRow['username']
        content.assignValue('username', username)

        return render(self.request, content.template, content.data)
