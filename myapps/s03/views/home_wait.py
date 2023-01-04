from .utils import *

class View(BaseMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        userId = int(request.session.get(sUser, 0))
        if not userId or userId == 0: return HttpResponseRedirect('/s03/')

        result = oConnExecute('SELECT username FROM users WHERE privilege=-3 AND id=' + str(userId))
        if not result: return HttpResponseRedirect('/s03/')
        username = result[0]
        
        #--- post
        
        action = request.POST.get('unlock', '')
        if action != '':
        
            oConnDoQuery('UPDATE users SET privilege=0 WHERE id=' + str(userId))
            return HttpResponseRedirect('/s03/')
        
        #--- get
        
        content = GetTemplate(self.request, 'home-wait')
        
        content.AssignValue('username', username)

        return render(self.request, content.template, content.data)
