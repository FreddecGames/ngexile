# -*- coding: utf-8 -*-

from django.db import connection

# retrieve universe
universe = "s03"

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

def oConnRow(query):
    cursor.execute(query)
    return dict_fetchone(cursor)

def oConnRows(query):
    cursor.execute(query)
    return dict_fetchall(cursor)

# return a quoted string for sql queries
def dosql(ch):
    ret = ch.replace('\\', '\\\\') 
    ret = ret.replace('\'', '\'\'')
    ret = '\'' + ret + '\''
    return ret

# return "null" if val is null or equals ''
def sqlValue(val):
    if val == None or val == "":
        return "Null"
    else:
        return str(val)

# tries to execute a query up to 3 times if it fails the first times
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
