from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

from django_registration import validators

from .lib import *


class StartForm(forms.Form):
    nickname = forms.CharField(max_length = 100)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        nickname_validators = [
            MinLengthValidator(5),
            UnicodeUsernameValidator(),
            validators.ReservedNameValidator(validators.DEFAULT_RESERVED_NAMES),
            validators.validate_confusables,
        ]
        self.fields['nickname'].validators.extend(nickname_validators)
    
    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        
        query = 'SELECT * FROM ng0.profiles WHERE name=' + strSql(nickname)
        result = dbRow(query)
        if result:
            raise forms.ValidationError(_('A player with that nickname already exists.'))
        
        return nickname
    
    def clean(self):
        super().clean()
        
        query = 'SELECT * FROM ng0.planets WHERE is_protected = true AND profile_id IS NULL'
        result = dbRow(query)
        if not result:
            raise forms.ValidationError(_('There is no more planet to start.'))
        
    
class View(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):        
        dbConnect()
        
        query = 'SELECT * FROM ng0.profiles WHERE user_id=' + str(request.user.id)
        result = dbRow(query)        
        if result:
            return HttpResponseRedirect('/ng0/')
            
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'ng0/game_start.html', {})

    def post(self, request):        
        form = StartForm(request.POST)
        if form.is_valid():

            dbExecute('SELECT ng0.profile_create(' + str(request.user.id) + ', ' + strSql(form.cleaned_data['nickname']) + ')')
            
            return HttpResponseRedirect('/ng0/')
        
        return render(request, 'ng0/game_start.html', { 'form':form })
        