from django.conf import settings
from django.shortcuts import redirect

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


def reset_password(request, uidb64, token):
    base_url = settings.FRONT_END.get('BASE_URL')
    path = settings.FRONT_END.get('FRONT_RESET_PWD_PATH')

    return redirect(f'{base_url}/{path}/{uidb64}/{token}/')


def confirm_account(request, token):
    base_url = settings.FRONT_END.get('BASE_URL')
    path = settings.FRONT_END.get('FRONT_CONFIRM_ACCOUNT_PATH')

    return redirect(f'{base_url}/{path}/{token}/')


class Profile(APIView):
    authentication_classes = [ TokenAuthentication ]
    permission_classes = [ IsAuthenticated ]

    def get(self, request, format=None):
        
        data = {}
        return Response(data)
        