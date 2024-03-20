# -*- coding: utf-8 -*-

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseView(APIView):
    
    def get(self, request, *args, **kwargs):
        
        #---
        
        data = { 'temp':1 }
        
        return Response(data)