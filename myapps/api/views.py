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

def dbRows(query):

    cursor.execute(query)
    return dict_fetchall(cursor)
    
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


class HomeStart(BaseView):

    def get(self, request, format=None):
        
        data = {}
        
        #---
        
        query = 'SELECT id, recommended' + \
                ' FROM sp_get_galaxy_info(' + str(self.userId) + ')'                
        rows = dbRows(query)
        
        data['galaxies'] = rows
        
        #---
        
        return Response(data)


class Layout(BaseView):

    def get(self, request, format=None):
        
        data = {}
        
        #---

        query = 'SELECT username, credits, prestige_points, lastplanetid, deletion_date, planets, score, previous_score, mod_planets, mod_commanders,' + \
                ' alliance_id, alliance_rank, leave_alliance_datetime IS NULL AND (alliance_left IS NULL OR alliance_left < now()) AS can_join_alliance,' + \
                ' credits_bankruptcy, orientation' + \
                ' FROM users' + \
                ' WHERE id=' + str(self.userId)        
        result = dbRow(query)

        data['username'] = result['username']
        data['profile_credits'] = result['credits']
        data['profile_prestige_points'] = result['prestige_points']
        data['profile_alliance_id'] = result['alliance_id']
        data['profile_alliance_rank'] = result['alliance_rank']
        data['delete_datetime'] = result['deletion_date']
        data['bankruptcy_hours'] = result['credits_bankruptcy']
        data['cur_planetid'] = result['lastplanetid']
        
        #---
        
        if data['profile_alliance_id']:
        
            query = 'SELECT label, leader, can_invite_player, can_kick_player, can_create_nap, can_break_nap, can_ask_money, can_see_reports, can_accept_money_requests, can_change_tax_rate, can_mail_alliance,' + \
                    ' can_manage_description, can_manage_announce, can_see_members_info, can_use_alliance_radars, can_order_other_fleets' + \
                    ' FROM alliances_ranks' + \
                    ' WHERE allianceid=' + str(data['profile_alliance_id']) + ' AND rankid=' + str(data['profile_alliance_rank'])
            result = dbRow(query)
            
            data['profile_alliance_rights'] = result
        
        #---
        
        query = 'SELECT (SELECT int4(COUNT(*)) FROM messages WHERE ownerid=' + str(self.userId) + ' AND read_date is NULL) AS new_mail,' + \
                '(SELECT int4(COUNT(*)) FROM reports WHERE ownerid=' + str(self.userId) + ' AND read_date is NULL AND datetime <= now()) AS new_report'
        result = dbRow(query)
        
        data['new_mail'] = result['new_mail']
        data['new_report'] = result['new_report']
        
        #---

        query = 'SELECT galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND id=' + str(data['cur_planetid']) + ' AND ownerid=' + str(self.userId)
        result = dbRow(query)
        
        data['cur_g'] = result['galaxy']
        data['cur_s'] = result['sector']
        data['cur_p'] = ((data['cur_planetid']  - 1) % 25) + 1
        
        #---
        
        if request.user.is_impersonate:
        
            data['impersonating'] = True
        
        #---
        
        return Response(data)
