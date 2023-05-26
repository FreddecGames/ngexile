# -*- coding: utf-8 -*-

import re

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View


################################################################################

maintenance = False

registration = { 'enabled':True, 'until':None }

################################################################################

class Template():
    
    def __init__(self, name):

        self.name = 'ng0/' + name + '.html'      
        self.data = {}

    def set(self, key, value=True):
    
        self.data[key] = value

    def render(self, request):
    
        return render(request, self.name, self.data)

################################################################################

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
    
def strSql(ch):

    ret = ch.replace('\\','\\\\') 
    ret = ret.replace('\'','\'\'')
    ret = '\'' + ret + '\''
    return ret

################################################################################

def isValidName(name):

    name = name.strip()

    if name == '' or len(name) < 4 or len(name) > 16:
        return False
    else:
    
        p = re.compile('^[a-zA-Z0-9\- ]+$')
        return p.match(name)
