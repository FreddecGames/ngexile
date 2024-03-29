# -*- coding: utf-8 -*-

from myapps.api.views._utils import *

from rest_framework import permissions

#---

class IsNotInMaintenance(permissions.BasePermission):

    ################################################################################

    def has_permission(self, request, view):
        
        #---
        
        if maintenance:        
            return False
        
        #---
        
        return True

#---

class IsRegistrationOpen(permissions.BasePermission):

    ################################################################################

    def has_permission(self, request, view):
        
        #---
        
        if not registration['enabled'] or (registration['until'] != None and timezone.now() > registration['until']):        
            return False
        
        #---
        
        return True

#---

class IsNew(permissions.BasePermission):

    ################################################################################

    def has_permission(self, request, view):
        
        dbConnect()
        
        #---
        
        query = 'SELECT privilege, resets' + \
                ' FROM users' + \
                ' WHERE id=' + str(request.user.id)
        row = dbRow(query)
        
        if not row or row['privilege'] != -3 or row['resets'] != 0:
            return False
        
        #---
        
        return True

#---

class IsWaiting(permissions.BasePermission):

    ################################################################################

    def has_permission(self, request, view):
        
        dbConnect()
        
        #---
        
        query = 'SELECT privilege, resets' + \
                ' FROM users' + \
                ' WHERE id=' + str(request.user.id)
        row = dbRow(query)
        
        if not row or row['privilege'] != -3 or row['resets'] == 0:
            return False
        
        #---
        
        return True

#---

class IsOnHolidays(permissions.BasePermission):

    ################################################################################

    def has_permission(self, request, view):
        
        dbConnect()
        
        #---
        
        query = 'SELECT privilege' + \
                ' FROM users' + \
                ' WHERE id=' + str(request.user.id)
        row = dbRow(query)
        
        if not row or row['privilege'] != -2:
            return False
        
        #---
        
        return True

#---

class IsGameover(permissions.BasePermission):

    ################################################################################

    def has_permission(self, request, view):
        
        dbConnect()
        
        #---
        
        query = 'SELECT planets, credits_bankruptcy' + \
                ' FROM users' + \
                ' WHERE id=' + str(request.user.id)
        row = dbRow(query)
        
        if not row or (profile['planets'] > 0 and profile['credits_bankruptcy'] > 0):
            return False
        
        #---
        
        return True

#---

class IsActive(permissions.BasePermission):

    ################################################################################

    def has_permission(self, request, view):
        
        dbConnect()
        
        #---
        
        query = 'SELECT privilege, planets, credits_bankruptcy' + \
                ' FROM users' + \
                ' WHERE id=' + str(request.user.id)
        row = dbRow(query)
        
        if not row or row['privilege'] != 0 or profile['planets'] <= 0 or profile['credits_bankruptcy'] <= 0:
            return False
        
        #---
        
        return True

#---

class HasAlliance(permissions.BasePermission):

    ################################################################################

    def has_permission(self, request, view):
        
        dbConnect()
        
        #---
        
        query = 'SELECT alliance_id' + \
                ' FROM users' + \
                ' WHERE id=' + str(request.user.id)
        row = dbRow(query)
        
        if not row or not row['alliance_id']:
            return False
        
        #---
        
        return True

#---

class HasNoAlliance(permissions.BasePermission):

    ################################################################################

    def has_permission(self, request, view):
        
        dbConnect()
        
        #---
        
        query = 'SELECT alliance_id' + \
                ' FROM users' + \
                ' WHERE id=' + str(request.user.id)
        row = dbRow(query)
        
        if not row or row['alliance_id']:
            return False
        
        #---
        
        return True

#---

class IsReportOwner(permissions.BasePermission):

    ################################################################################

    def has_object_permission(self, request, view, obj):
        
        if not obj or obj['userid'] != request.user.id:
            return False
        
        #---
        
        return True
