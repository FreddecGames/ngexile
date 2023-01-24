# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.views import View

from myapps.s03.lib.exile import *

class View(ExileMixin, View):

    def dispatch(self, request, *args, **kwargs):
        
        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
    
        return self.connect(request)
    
    def connect(self, request):
        
        '''
        var url = urlNexus + 'authenticate.asp?id=' + Request.Cookies('authID') + '&address=' + Request.ServerVariables("REMOTE_ADDR");

        var xml = Server.CreateObject("MSXML2.ServerXMLHTTP");

        var resultData = {};

        try {
            xml.open("GET", url, true); // True specifies an asynchronous request
            xml.send();

            // Wait for up to 3 seconds if we've not gotten the data yet
            if(xml.readyState != 4)
                xml.waitForResponse(3);

            if(xml.readyState == 4 && xml.status == 200) {
                resultData = eval('(' + xml.responseText + ')');
            }
            else {
                // Abort the XMLHttp request
                xml.abort();

                resultData = {userid:null, error:'Problem communicating with remote server...' }
            }
        } catch(e) {
            resultData = {userid:null, error:e.message }
        }
        '''
        
        if request.user.is_authenticated:
            '''
            Session.LCID = resultData.lcid;
            '''
            
            rs = oConnExecute('SELECT id, lastplanetid, privilege, resets FROM sp_account_connect(' + str(request.user.id) + ', 1036,' + dosql(self.ipaddress) + ',' + dosql(self.forwardedfor) + ',' + dosql(self.useragent) + ', 0)');

            request.session[sUser] = rs[0]
            request.session[sPlanet] = rs[1]
            request.session[sPrivilege] = rs[2]
            request.session[sLogonUserID] = rs[0]
            
            if not request.session.get("isplaying"):
                request.session["isplaying"] = True
                '''
                Application.lock();
                Application("players") = Application("players") + 1;
                Application.unlock();
                '''
            '''
            Application("usersession" + rs(0).Value) = Session.SessionID;
            '''
            
            result = oConnExecute('SELECT username FROM users WHERE id=' + str(rs[0]))
            try:
                if not result[0]: oConnDoQuery('UPDATE users SET username=' + dosql(request.user.username) + ' WHERE username IS NULL AND id=' + str(rs[0]))
            except:
                return HttpResponseRedirect("/s03/start/")
                
            if(rs[2] == -3):
                return HttpResponseRedirect("/s03/wait/")
            elif(rs[2] == -2):
                return HttpResponseRedirect("/s03/holidays/")
            elif(rs[2] < 100 and rs[3] == 0):
                return HttpResponseRedirect("/s03/start/")
            else:
                return HttpResponseRedirect("/s03/overview/")
                
        return HttpResponseRedirect(urlNexus)
