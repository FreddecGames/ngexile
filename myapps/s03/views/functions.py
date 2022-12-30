# -*- coding: utf-8 -*-

class BaseMixin:

    SessionEnabled = False

    def pre_dispatch(self, request, *args, **kwargs):

        try:
            request.session["test"] = "test"
            self.SessionEnabled = True
        except:
            pass
        
        self.lang = request.GET.get("lang", "")
        
        self.ipaddress = request.META.get("REMOTE_ADDR", "")
        self.forwardedfor = request.META.get("HTTP_X_FORWARDED_FOR", "")
        self.useragent = request.META.get("HTTP_USER_AGENT", "")

def ToStr(s):
    if s: return str(s)
    else: return ''

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
