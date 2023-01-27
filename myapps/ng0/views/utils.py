import re
import math

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

#--- SQL functions

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
    
def dbExecute(query):
    cursor.execute(query)

def dbRow(query):
    cursor.execute(query)
    return dictFetchOne(cursor)

def dbRows(query):
    cursor.execute(query)
    return dictFetchAll(cursor)

#--- Template functions

class TemplaceContext():
    
    def __init__(self):
    
        self.template = ''
        self.data = {}

    def setValue(self, key, value):
    
        self.data[key] = value

def getTemplate(request, name):

    result = TemplaceContext()
    
    result.template = 'ng0/' + name + '.html'
    
    result.setValue('STATIC_PATH', '/static/ng0/')
    
    return result

#--- Check functions

def isValidUsername(username):

    if username == '' or len(username) < 4 or len(username) > 16:
        return False
    else:
        p = re.compile('^[a-zA-Z0-9]+([ ]?[\-]?[ ]?[a-zA-Z0-9]+)*$')
        return p.match(username)
