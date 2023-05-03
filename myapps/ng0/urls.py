from django.urls import path
from django.views.generic.base import RedirectView

from .views import empire_view


urlpatterns = [

	path('empire-overview/', empire_view.View.as_view()),
    
	path('', RedirectView.as_view(url='/ng0/empire-overview')),
]
