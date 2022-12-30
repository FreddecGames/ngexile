# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .exile import *
from .template import *

class View(View):

    def dispatch(self, request, *args, **kwargs):

        #
        # process page
        #

        return self.DisplayPage()

    def sqlValue(self, value):
        if value == None:
            sqlValue = "None"
        else:
            sqlValue = "'" + value + "'"

    #
    # display page
    #
    def DisplayPage(self):

        content = GetTemplate(self.request, "maintenance")
        content.AssignValue("skin", "s_transparent")

        return render(self.request, content.template, content.data)
