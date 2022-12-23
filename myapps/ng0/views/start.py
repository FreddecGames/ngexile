from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from django_registration import validators

from ._lib import *


class StartForm(forms.Form):
    nickname = forms.CharField(max_length=100)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        nickname_validators = [
            MinLengthValidator(5),
            UnicodeUsernameValidator(),
            validators.ReservedNameValidator(validators.DEFAULT_RESERVED_NAMES),
            validators.validate_confusables,
        ]
        self.fields['nickname'].validators.extend(nickname_validators)
    
    
class View(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        
        query = 'SELECT *' +\
                ' FROM ' + serverId + '.profiles' +\
                ' WHERE user_id=' + str(request.user.id)
        result = dbRow(query)
        
        if result:
            return HttpResponseRedirect('/' + serverId + '/')
            
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        
        data = {}
        return render(request, 'ng0/start.html', data)

    def post(self, request):
        
        form = StartForm(request.POST)
        if form.is_valid():

            query = 'INSERT INTO ' + serverId + '.profiles(user_id, nickname)' +\
                    ' VALUES(' + str(request.user.id) + ',\'' + form.cleaned_data['nickname'] + '\')'
            dbExecute(query)
            
            return HttpResponseRedirect('/' + serverId + '/')
        
        return render(request, 'ng0/start.html', { 'form':form })
        