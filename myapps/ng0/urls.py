from django.urls import path
from django.views.generic.base import RedirectView

from .views import report_battle


urlpatterns = [

	path('report-battle/', report_battle.View.as_view()),
]
