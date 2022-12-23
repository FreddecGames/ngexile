from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from ._lib import *
    
    
class View(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        
        query = 'SELECT *' +\
                ' FROM ' + serverId + '.profiles' +\
                ' WHERE user_id=' + str(request.user.id)
        result = dbRow(query)
        
        if result == None:
            return HttpResponseRedirect('/' + serverId + '/start')
            
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        
        data = {}
        return render(request, serverId + '/home.html', data)
