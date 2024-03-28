# -*- coding: utf-8 -*-

import math
import re
import time

from random import *

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

registration = { 'enabled':True, 'until':None }

maintenance = False

rWar = -2
rHostile = -1
rFriend = 0
rAlliance = 1
rSelf = 2

#---

def isValidName(myName):

    myName = myName.strip()

    if myName == '' or len(myName) < 2 or len(myName) > 12:
        return False
    else:
    
        p = re.compile('^[a-zA-Z0-9]+([ ]?[\-]?[ ]?[a-zA-Z0-9]+)*$')
        return p.match(myName)


def isValidURL(myURL):

    myURL = myURL.strip()

    p = re.compile('^(http|https|ftp)\://([a-zA-Z0-9\.\-]+(\:[a-zA-Z0-9\.&%\$\-]+)*@)?((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.[a-zA-Z]{2,4})(\:[0-9]+)?(/[^/][a-zA-Z0-9\.\,\?\'\\/\+&%\$#\=~_\-@]*)*$')
    return p.match(myURL)


def isValidObjectName(myName):

    myName = myName.strip()

    if myName == '' or len(myName) < 2 or len(myName) > 16:
        return False
    else:
    
        p = re.compile('^[a-zA-Z0-9\- ]+$')
        return p.match(myName)

def isValidAllianceName(myName):
    
    myName = myName.strip()
    
    if myName == '' or len(myName) < 4 or len(myName) > 32:
        return False
    else:
    
        p = re.compile('^[a-zA-Z0-9]+([ ]?[.]?[\-]?[ ]?[a-zA-Z0-9]+)*$')
        return p.match(myName)

def isValidAllianceTag(myTag):
    
    myTag = myTag.strip()
    
    if myTag == '' or len(myTag) < 2 or len(myTag) > 4:
        return False
    else:
    
        p = re.compile('^[a-zA-Z0-9]+$')
        return p.match(myTag)

def isValidCategoryName(myName):
    
    myName = myName.strip()
    
    if myName == '' or len(myName) < 2 or len(myName) > 32:
        return False
    else:
    
        p = re.compile('^[a-zA-Z0-9\- ]+$')
        return p.match(myName)

#---

def ToStr(s, defaultValue=''):
 
    if (s == '' or s == None): return defaultValue
    return s.strip()

def ToInt(s, defaultValue):
 
    if (s == '' or s == None): return defaultValue
    i = int(float(s))
    if i == None: return defaultValue
    return i

def ToBool(s, defaultValue):

    if (s == '' or s == '' or s == None): return defaultValue
    i = int(float(s))
    if i == 0: return defaultValue
    return True

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

def dbExecute(query):

    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) > 0: return results[0][0]
    return None

def dosql(ch):

    ret = ch.replace('\\', '\\\\') 
    ret = ret.replace('\'', '\'\'')
    ret = '\'' + ret + '\''
    return ret

def sqlValue(val):

    if val == None or val == '': return 'Null'
    else: return str(val)

#---

def getPercent(current, max, slice):

    if current >= max or max == 0: return 100
    else: return slice * int(100 * current / max / slice)

#---

class Template():
    
    def __init__(self):

        self.data = {}

    def set(self, key, value=True):
    
        self.data[key] = value
        
def getTemplate():

    result = Template()

    return result

#---

class BaseView(APIView):
    authentication_classes = [ TokenAuthentication ]
    showHeader = False

    def initial(self, request, *args, **kwargs):
        super(BaseView, self).initial(request, *args, **kwargs)
        
        #---
        
        self.userId = request.user.id
        
        #---
        
        dbConnect()
        
        #---

        ipaddress = request.META.get('REMOTE_ADDR', '')
        useragent = request.META.get('HTTP_USER_AGENT', '')
        forwardedfor = request.META.get('HTTP_X_FORWARDED_FOR', '')
        
        dbQuery('SELECT * FROM sp_account_connect(' + str(self.userId) + ', 1036,' + dosql(ipaddress) + ',' + dosql(forwardedfor) + ',' + dosql(useragent) + ', 0)')
        
        #---
        
        query = 'SELECT username, privilege, resets, credits, lastplanetid, deletion_date, planets, score, previous_score, mod_planets, mod_commanders,' + \
                ' alliance_id, alliance_rank, leave_alliance_datetime IS NULL AND (alliance_left IS NULL OR alliance_left < now()) AS can_join_alliance,' + \
                ' credits_bankruptcy, orientation, prestige_points' + \
                ' FROM users' + \
                ' WHERE id=' + str(self.userId)
        self.profile = dbRow(query)
        
        #---
        
        self.allianceId = self.profile['alliance_id']
        self.allianceRankId = self.profile['alliance_rank']
        
        #---
            
        self.allianceRights = None
        
        if self.allianceId and self.allianceRankId:
        
            query = 'SELECT label, leader, can_invite_player, can_kick_player, can_create_nap, can_break_nap, can_ask_money, can_see_reports, can_accept_money_requests, can_change_tax_rate, can_mail_alliance,' + \
                    ' can_manage_description, can_manage_announce, can_see_members_info, can_use_alliance_radars, can_order_other_fleets' + \
                    ' FROM alliances_ranks' + \
                    ' WHERE allianceid=' + str(self.allianceId) + ' AND rankid=' + str(self.allianceRankId)
            self.allianceRights = dbRow(query)
        
        #---
        
        if self.profile['lastplanetid'] == None or  self.profile['lastplanetid'] == '':
        
            planet = dbRow('SELECT id, galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=' + str(self.userId) + ' LIMIT 1')
            if planet:
            
                dbQuery('UPDATE users SET lastplanetid=' + str(planet['id']) + ' WHERE id=' + str(self.userId))
                self.profile['lastplanetid'] = planet['id']

        #---
        
        if self.profile['lastplanetid'] != None and self.profile['lastplanetid'] != '':
        
            planet = dbRow('SELECT id, galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=' + str(self.userId) + ' LIMIT 1')    
            
            self.currentPlanetId = planet['id']
            self.currentPlanetGalaxy = planet['galaxy']
            self.currentPlanetSector = planet['sector']
