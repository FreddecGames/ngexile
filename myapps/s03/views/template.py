# -*- coding: utf-8 -*-

from .functions import *

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

    result.AssignValue("PATH_IMAGES", "/static/assets/")
    result.AssignValue("PATH_TEMPLATE", "/s03/templates")

    return result