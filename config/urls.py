from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django_registration.backends.activation.views import RegistrationView

from myapps.accounts.forms import UserRegistrationForm


urlpatterns = [

    path('admin/', admin.site.urls),
    
    path('impersonate/', include('impersonate.urls')),
    
    path('i18n/', include('django.conf.urls.i18n')),
    
    path('accounts/register/', RegistrationView.as_view(form_class = UserRegistrationForm), name='django_registration_register'),    
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('lobby/', include('myapps.lobby.urls')),
    path('s03/', include('myapps.s03.urls')),
    
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
