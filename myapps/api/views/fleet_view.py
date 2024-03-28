# -*- coding: utf-8 -*-

from myapps.api.views._utils import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated ]
    
    
    def post(self, request, format=None):
        
        data = {}

        #---
        
        action = request.data['action']

        #---
        
        if action == '':
                      
            return Response(data)
            
        #---
        
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, format=None):
        
        data = {}
        
        #---
        
        return Response(data)
