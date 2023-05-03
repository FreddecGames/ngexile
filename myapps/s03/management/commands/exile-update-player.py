# -*- coding: utf_8 -*-

import time

from django.core.management.base import BaseCommand
from django.utils import timezone

from myapps.s03.views._utils import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        h = timezone.now().hour
        connectDB()
        rows = dbRows("SELECT id FROM users WHERE privilege >= 0 AND planets > 0 AND credits_bankruptcy > 0 AND lastlogin IS NOT NULL ORDER BY id")
        for row in rows:
            dbExecute("SELECT sp_update_player(" + str(row['id']) + "," + str(h) + ");")
            time.sleep(20)
