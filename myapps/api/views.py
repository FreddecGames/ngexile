from django.conf import settings
from django.db import connection
from django.shortcuts import redirect

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

#---

def reset_password(request, uidb64, token):
    base_url = settings.FRONT_END.get('BASE_URL')
    path = settings.FRONT_END.get('FRONT_RESET_PWD_PATH')

    return redirect(f'{base_url}/{path}/{uidb64}/{token}/')


def confirm_account(request, token):
    base_url = settings.FRONT_END.get('BASE_URL')
    path = settings.FRONT_END.get('FRONT_CONFIRM_ACCOUNT_PATH')

    return redirect(f'{base_url}/{path}/{token}/')

#---

def dict_fetchall(cursor):

    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def dict_fetchone(cursor):

    results = dict_fetchall(cursor)
    if results: return results[0]
    else: return None

cursor = None

def dbConnect():

    global cursor
    cursor = connection.cursor()
    
def dbQuery(query):

    cursor.execute(query)

def dbRow(query):

    cursor.execute(query)
    return dict_fetchone(cursor)

def dosql(ch):

    ret = ch.replace('\\', '\\\\') 
    ret = ret.replace('\'', '\'\'')
    ret = '\'' + ret + '\''
    return ret

#---

class BaseView(APIView):
    authentication_classes = [ TokenAuthentication ]
    permission_classes = [ IsAuthenticated ]

    def initial(self, request, *args, **kwargs):
        super(BaseView, self).initial(request, *args, **kwargs)
        
        self.userId = request.user.id
        
        dbConnect()

        ipaddress = request.META.get('REMOTE_ADDR', '')
        useragent = request.META.get('HTTP_USER_AGENT', '')
        forwardedfor = request.META.get('HTTP_X_FORWARDED_FOR', '')
        
        dbQuery('SELECT * FROM sp_account_connect(' + str(self.userId) + ', 1036,' + dosql(ipaddress) + ',' + dosql(forwardedfor) + ',' + dosql(useragent) + ', 0)')


class Profile(BaseView):

    def get(self, request, format=None):
        
        query = 'SELECT username, privilege, resets, credits, lastplanetid, deletion_date, planets, score, previous_score, mod_planets, mod_commanders,' + \
                ' alliance_id, alliance_rank, leave_alliance_datetime IS NULL AND (alliance_left IS NULL OR alliance_left < now()) AS can_join_alliance,' + \
                ' credits_bankruptcy, orientation, prestige_points' + \
                ' FROM users' + \
                ' WHERE id=' + str(self.userId)
        
        data = dbRow(query)
        return Response(data)
        