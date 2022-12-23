from django.urls import path

from .views import home, start


urlpatterns = [

    path('', home.View.as_view()),
    path('start/', start.View.as_view()),
]
