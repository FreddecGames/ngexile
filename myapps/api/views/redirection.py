# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---

def reset_password(request, uidb64, token):

    base_url = settings.FRONT_END.get('BASE_URL')
    path = settings.FRONT_END.get('FRONT_RESET_PWD_PATH')

    return redirect(f'{base_url}/{path}/{uidb64}/{token}/')

#---

def confirm_account(request, token):

    base_url = settings.FRONT_END.get('BASE_URL')
    path = settings.FRONT_END.get('FRONT_CONFIRM_ACCOUNT_PATH')

    return redirect(f'{base_url}/{path}/{token}/')
