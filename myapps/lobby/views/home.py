from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from socket import getaddrinfo, SOCK_STREAM


class View(LoginRequiredMixin, View):

    def get(self, request):    
        return render(request, 'lobby/home.html')
