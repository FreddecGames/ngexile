# -*- coding: utf-8 -*-

import re

#functions used in username, register, password.asp & options.asp

#validate name (alphanumeric + space), len 2-12
def isValidName(myName):

    if myName == "" or len(myName) < 2 or len(myName) > 12:
        return False
    else:
        p = re.compile("^[a-zA-Z0-9]+([ ]?[\-]?[ ]?[a-zA-Z0-9]+)*$")

        return p.match(myName)

# validate an url
def isValidURL(myURL):

    p = re.compile("^(http|https|ftp)\://([a-zA-Z0-9\.\-]+(\:[a-zA-Z0-9\.&%\$\-]+)*@)?((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.[a-zA-Z]{2,4})(\:[0-9]+)?(/[^/][a-zA-Z0-9\.\,\?\'\\/\+&%\$#\=~_\-@]*)*$")

    return p.match(myURL)

# return if the given name if valid for a fleet, a planet
def isValidObjectName(myName):
    myName = myName.strip()

    if myName == "" or len(myName) < 2 or len(myName) > 16:
        return False
    else:
        p = re.compile("^[a-zA-Z0-9\- ]+$")

        return p.match(myName)
