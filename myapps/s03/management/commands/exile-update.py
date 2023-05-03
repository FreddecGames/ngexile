# -*- coding: utf_8 -*-

import time
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from myapps.s03.views._utils import *

class Command(BaseCommand):

    def handle(self, *args, **options):

        #---
        
        connectDB()

        #---
        
        start = timezone.now()
        while timezone.now() - start < timedelta(seconds=55):
        
            #---
            
            dbQuery("SELECT sp_execute_processes()")
            
            #---
        
            time.sleep(0.5)
