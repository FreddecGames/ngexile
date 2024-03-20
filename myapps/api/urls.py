# -*- coding: utf-8 -*-

from django.urls import path

from .views import init


urlpatterns = [

    path('init/', init.BaseView.as_view()),
]