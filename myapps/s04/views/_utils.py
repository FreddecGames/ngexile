# -*- coding: utf-8 -*-

import re

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext
from django.views import View

registration = True
maintenance = False

#---

def isValidName(myName):

    myName = myName.strip()

    if myName == '' or len(myName) < 4 or len(myName) > 16:
        return False
    else:
    
        p = re.compile('^[a-zA-Z0-9]+([ ]?[\-]?[ ]?[a-zA-Z0-9]+)*$')
        return p.match(myName)

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

class TemplateContext():
    
    def __init__(self):

        self.template = ''        
        self.data = {}

    def set(self, key, value=True):
    
        self.data[key] = value
        
def getTemplate(request, name):

    result = TemplateContext()

    result.template = 's04/' + name + '.html'

    return result

#---

class BaseView(LoginRequiredMixin, View):

    def pre_dispatch(self, request, *args, **kwargs):
        
        #--- 
        
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')

        self.userId = request.user.id
        
        #---
        
        if maintenance and not request.user.is_superuser: return HttpResponseRedirect('/s04/home-maintenance/')
        
        #---
        
        dbConnect()
