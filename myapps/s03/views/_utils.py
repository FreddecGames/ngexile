# -*- coding: utf-8 -*-

import math
import re
import time

from random import *

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import View

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

class TemplateContext():
    
    def __init__(self):

        self.template = ''        
        self.data = {}

    def set(self, key, value=True):
    
        self.data[key] = value
        
def getTemplate(request, name):

    result = TemplateContext()

    result.template = 's03/' + name + '.html'

    result.set('PATH_IMAGES', '/static/s03/')

    return result

#---

class BaseView(LoginRequiredMixin, View):

    def pre_dispatch(self, request, *args, **kwargs):
        
        #--- 
        
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')

        self.userId = request.user.id
        
        #---
        
        if maintenance: return HttpResponseRedirect('/s03/maintenance/')
        
        #---
        
        dbConnect()
