# imports

import re

from math import sqrt

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.utils import timezone

# relations

rUninhabited = -3
rWar = -2
rHostile = -1
rFriend = 0
rAlliance = 1
rSelf = 2

# session constant names

sUser = "user"
sPlanet = "planet"

# SQL functions

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

def dosql(ch):
    ret = ch.replace('\\', '\\\\') 
    ret = ret.replace('\'', '\'\'')
    ret = '\'' + ret + '\''
    return ret

def sqlValue(val):
    if val == None or val == "":
        return "Null"
    else:
        return str(val)

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

# cast functions

def ToInt(s, defaultValue):
    if(s == "" or s == '' or s == None): return defaultValue
    i = int(float(s))
    if i == None:
        return defaultValue
    return i

def ToBool(s, defaultValue):
    if(s == "" or s == '' or s == None): return defaultValue
    i = int(float(s))
    if i == 0:
        return defaultValue
    return True

# base mixin

class BaseMixin(LoginRequiredMixin):

    def pre_dispatch(self, request, *args, **kwargs):
        
        connectDB()

# template functions

class TemplaceContext():
    
    def __init__(self):
    
        self.template = ""        
        self.data = {}

    def AssignValue(self, key, value):
        self.data[key] = value
    
    def Parse(self, key):
        self.data[key] = True
        
def GetTemplate(request, name):

    result = TemplaceContext()

    result.template = "s03/" + name + ".html"

    result.AssignValue("PATH_IMAGES", "/static/s03/img/")

    return result

# standard SQL requests

def retrieveBuildingsCache():
    
    query = "SELECT id, storage_workers, energy_production, storage_ore, storage_hydrocarbon, workers, storage_scientists, storage_soldiers, label, description, energy_consumption, workers*maintenance_factor/100, upkeep FROM db_buildings"
    return oConnExecute(query)

def retrieveBuildingsReqCache():
    
    query = "SELECT buildingid, required_buildingid" +\
            " FROM db_buildings_req_building" +\
            "    INNER JOIN db_buildings ON (db_buildings.id=db_buildings_req_building.buildingid)" +\
            " WHERE db_buildings.destroyable"
    return oConnExecute(query)

def retrieveShipsCache():

    query = "SELECT id, label, description FROM db_Ships ORDER BY category, id"
    return oConnExecute(query)

def retrieveShipsReqCache():
    
    query = "SELECT shipid, required_buildingid FROM db_ships_req_building"
    return oConnExecute(query)

def retrieveResearchCache():

    query = "SELECT id, label, description FROM db_Research"
    return oConnExecute(query)

def checkPlanetListCache(Session):
    
    query = "SELECT id, name, galaxy, sector, planet FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=" + str(Session.get("user")) + " ORDER BY id"
    return oConnExecuteAll(query)

def getBuildingLabel(buildingid):
    for i in retrieveBuildingsCache():
        if buildingid == i[0]:
            return i[8]

def getBuildingDescription(buildingid):
    for i in retrieveBuildingsCache():
        if buildingid == i[0]:
            return i[9]

def getShipLabel(ShipId):
    for i in retrieveShipsCache():
        if ShipId == i[0]:
            return i[1]

def getShipDescription(ShipId):
    for i in retrieveShipsCache():
        if ShipId == i[0]:
            return i[2]

def getResearchLabel(ResearchId):
    for i in retrieveResearchCache():
        if ResearchId == i[0]:
            return i[1]

def getResearchDescription(ResearchId):
    for i in retrieveResearchCache():
        if ResearchId == i[0]:
            return i[2]

# standard string checks

def isValidName(myName):

    if myName == "" or len(myName) < 2 or len(myName) > 12:
        return False
    else:
        p = re.compile("^[a-zA-Z0-9]+([ ]?[\-]?[ ]?[a-zA-Z0-9]+)*$")
        return p.match(myName)

def isValidURL(myURL):

    p = re.compile("^(http|https|ftp)\://([a-zA-Z0-9\.\-]+(\:[a-zA-Z0-9\.&%\$\-]+)*@)?((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.[a-zA-Z]{2,4})(\:[0-9]+)?(/[^/][a-zA-Z0-9\.\,\?\'\\/\+&%\$#\=~_\-@]*)*$")
    return p.match(myURL)

def isValidObjectName(myName):

    myName = myName.strip()

    if myName == "" or len(myName) < 2 or len(myName) > 16:
        return False
    else:
        p = re.compile("^[a-zA-Z0-9\- ]+$")
        return p.match(myName)
