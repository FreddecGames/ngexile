from .utils import *

class View(BaseMixin, View):

    def dispatch(self, request, *args, **kwargs):
        
        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        if not request.user.id: return HttpResponseRedirect('/')
        
        ipaddress = request.META.get('REMOTE_ADDR', '')
        useragent = request.META.get('HTTP_USER_AGENT', '')
        forwardedfor = request.META.get('HTTP_X_FORWARDED_FOR', '')

        rs = oConnExecute('SELECT id, lastplanetid, privilege, resets FROM sp_account_connect(' + str(request.user.id) + ', 1036,' + dosql(ipaddress) + ',' + dosql(forwardedfor) + ',' + dosql(useragent) + ', 0)')
        
        request.session[sUser] = rs[0]
        
        result = oConnExecute('SELECT username FROM users WHERE id=' + str(rs[0]))
        if not result[0]: return HttpResponseRedirect('/s03/home-start/')
        
        if (rs[2] == -3): return HttpResponseRedirect('/s03/home-wait/')
        elif (rs[2] == -2): return HttpResponseRedirect('/s03/home-holidays/')
        elif (rs[2] < 100 and rs[3] == 0): return HttpResponseRedirect('/s03/home-start/')
            
        return HttpResponseRedirect('/s03/empire-view/')

