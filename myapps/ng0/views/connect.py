from .utils import *

class View(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        
        dbConnect()
        
        if not request.user.is_anonymous: return HttpResponseRedirect('/')
        
        ipaddress = request.META.get('REMOTE_ADDR', '')
        useragent = request.META.get('HTTP_USER_AGENT', '')
        forwardedfor = request.META.get('HTTP_X_FORWARDED_FOR', '')

        user = dbRow('SELECT id, privilege FROM sp_account_connect(' + str(request.user.id) + ', 1036,' + strSql(ipaddress) + ',' + strSql(forwardedfor) + ',' + strSql(useragent) + ', 0)')
        
        result = dbRow('SELECT username FROM users WHERE id=' + str(request.user.id))
        if not result['username']: return HttpResponseRedirect('/s03/home-start/')
        
        if (user['privilege'] == -3): return HttpResponseRedirect('/s03/home-wait/')
        elif (user['privilege'] == -2): return HttpResponseRedirect('/s03/home-holidays/')
            
        return HttpResponseRedirect('/s03/empire-view/')

