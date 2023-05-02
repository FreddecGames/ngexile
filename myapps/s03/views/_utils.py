# -*- coding: utf-8 -*-

import re
import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect

registration = { "enabled":True, "until":None }

maintenance = False

rWar = -2
rHostile = -1
rFriend = 0
rAlliance = 1
rSelf = 2

#--- string check functions

def isValidName(myName):

    myName = myName.strip()

    if myName == "" or len(myName) < 2 or len(myName) > 12:
        return False
    else:
    
        p = re.compile("^[a-zA-Z0-9]+([ ]?[\-]?[ ]?[a-zA-Z0-9]+)*$")
        return p.match(myName)


def isValidURL(myURL):

    myURL = myURL.strip()

    p = re.compile("^(http|https|ftp)\://([a-zA-Z0-9\.\-]+(\:[a-zA-Z0-9\.&%\$\-]+)*@)?((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.[a-zA-Z]{2,4})(\:[0-9]+)?(/[^/][a-zA-Z0-9\.\,\?\'\\/\+&%\$#\=~_\-@]*)*$")
    return p.match(myURL)


def isValidObjectName(myName):

    myName = myName.strip()

    if myName == "" or len(myName) < 2 or len(myName) > 16:
        return False
    else:
    
        p = re.compile("^[a-zA-Z0-9\- ]+$")
        return p.match(myName)

def isValidAllianceName(myName):
    
    myName = myName.strip()
    
    if myName == "" or len(myName) < 4 or len(myName) > 32:
        return False
    else:
    
        p = re.compile("^[a-zA-Z0-9]+([ ]?[.]?[\-]?[ ]?[a-zA-Z0-9]+)*$")
        return p.match(myName)

def isValidAllianceTag(myTag):
    
    myTag = myTag.strip()
    
    if myTag == "" or len(myTag) < 2 or len(myTag) > 4:
        return False
    else:
    
        p = re.compile("^[a-zA-Z0-9]+$")
        return p.match(myTag)

def isValidCategoryName(myName):
    
    myName = myName.strip()
    
    if myName == "" or len(myName) < 2 or len(myName) > 32:
        return False
    else:
    
        p = re.compile("^[a-zA-Z0-9\- ]+$")
        return p.match(myName)

#--- cast functions

def ToInt(s, defaultValue):
 
    if (s == "" or s == '' or s == None): return defaultValue
    i = int(float(s))
    if i == None: return defaultValue
    return i

def ToBool(s, defaultValue):

    if (s == "" or s == '' or s == None): return defaultValue
    i = int(float(s))
    if i == 0: return defaultValue
    return True

#--- SQL functions

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

def connectDB():

    global cursor
    cursor = connection.cursor()

def oConnExecute(query):

    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) > 1: return results
    elif results: return results[0]
    return None

def oConnExecuteAll(query):

    cursor.execute(query)
    return cursor.fetchall()
    
def oConnDoQuery(query):

    cursor.execute(query)
    
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

def dbResults(query):

    cursor.execute(query)
    results = cursor.fetchall()
    return results

def dosql(ch):

    ret = ch.replace('\\', '\\\\') 
    ret = ret.replace('\'', '\'\'')
    ret = '\'' + ret + '\''
    return ret

def sqlValue(val):

    if val == None or val == "": return "Null"
    else: return str(val)

def connExecuteRetry(query):

    i = 0
    while i < 5:
        try:
            i = 10
            rs = oConnExecute(query)
            return rs
        except:
            i = i + 1
    return None
    
def connExecuteRetryNoRecords(query):

    i = 0
    while i < 5:
        try:
            i = 10
            oConnExecute(query)
        except:
            i = i + 1

#--- template functions

class TemplaceContext():
    
    def __init__(self):

        self.template = ""        
        self.data = {}

    def setValue(self, key, value):
        self.data[key] = value
    
    def Parse(self, key):
        self.data[key] = True
        
def getTemplate(request, name):

    result = TemplaceContext()

    result.template = name + ".html"

    result.setValue("PATH_IMAGES", "/static/s03/")

    return result

#--- mixin

class ExileMixin(LoginRequiredMixin):

    def pre_dispatch(self, request, *args, **kwargs):
        
        #---
        
        if maintenance: return HttpResponseRedirect('/s03/maintenance/')
        
        #---
        
        connectDB()
