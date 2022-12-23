from django.urls import path

from .views import home


urlpatterns = [

    path('', home.View.as_view()),
]
