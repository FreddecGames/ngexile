# -*- coding: utf-8 -*-

import re
import math

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

#---

maintenance = False

#---

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
    
cursor = None

def dbConnect():
    global cursor
    cursor = connection.cursor()
    
def dbQuery(query):
    cursor.execute(query)

def dbExecute(query):
    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) > 0: return results[0][0]
    return None

def dbRow(query):
    cursor.execute(query)
    return dictFetchOne(cursor)

def dbRows(query):
    cursor.execute(query)
    return dictFetchAll(cursor)

#---

class Template():
    
    def __init__(self):
    
        self.name = ''
        self.data = {}

    def setValue(self, key, value):
    
        self.data[key] = value

def getTemplate(request, name):

    result = Template()
    
    result.name = 'ng0/' + name + '.html'
    
    result.setValue('STATIC_PATH', '/static/ng0/')
    
    return result
