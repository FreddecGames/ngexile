from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView


urlpatterns = [

	path('', RedirectView.as_view(url='/ng0/home/')),
    
    path('home/', TemplateView.as_view(template_name='ng0/home.html')),
]
