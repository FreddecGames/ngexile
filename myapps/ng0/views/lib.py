def strSql(str):
    ret = str.replace('\\', '\\\\') 
    ret = ret.replace('\'', '\'\'')
    ret = '\'' + ret + '\''
    return ret

def dictFetchAll(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def dictFetchOne(cursor):
    results = dictFetchAll(cursor)
    if results: return results[0]
    else: return None


from django.db import connection


cursor = None

def dbConnect():
    global cursor
    cursor = connection.cursor()
    print(cursor)
    
def dbExecute(query):
    cursor.execute(query)
    
def dbRow(query):
    cursor.execute(query)
    return dictFetchOne(cursor)

def dbRows(query):
    cursor.execute(query)
    return dictFetchAll(cursor)


from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View


class ExileView(LoginRequiredMixin, View):

    profile = None
    curPlanet = None

    def dispatch(self, request, *args, **kwargs):
    
        dbConnect()
        
        query = 'SELECT * FROM ng0.profiles WHERE user_id=' + str(request.user.id)
        self.profile = dbRow(query)        
        if self.profile == None:
            return HttpResponseRedirect('/ng0/start')        
        
        if self.profile['curplanet_id'] == None:        
            query = 'SELECT * FROM ng0.planets WHERE profile_id=' + str(self.profile['id']) + ' ORDER BY sector, number LIMIT 1'
            self.curPlanet = dbRow(query)            
            if self.curPlanet:
                dbExecute('UPDATE ng0.profiles' + ' SET curplanet_id=' + str(self.curPlanet['id']) + ' WHERE id=' + str(self.profile['id']))
                
        else:
            query = 'SELECT * FROM ng0.planets WHERE id=' + str(self.profile['curplanet_id'])
            self.curPlanet = dbRow(query)
        
        return super().dispatch(request, *args, **kwargs)
        
    def display(self, request, template, data):
        
        data['profile'] = self.profile
        data['curPlanet'] = self.curPlanet
        
        return render(request, template, data)
