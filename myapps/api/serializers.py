from dj_rest_auth.registration.serializers import RegisterSerializer

from rest_framework import serializers


class UserRegisterSerializer(RegisterSerializer):

    username = serializers.EmailField(required=True)
