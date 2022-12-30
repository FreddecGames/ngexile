import time

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from myapps.ng0.views.lib import *


class Command(BaseCommand):

    def handle(self, *args, **options):
    
        dbConnect()
        
        start = timezone.now()
        while timezone.now() - start < timedelta(seconds=55):
            dbExecute('SELECT ng0.server_update()')
            time.sleep(0.5)
