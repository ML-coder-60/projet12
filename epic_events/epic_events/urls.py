"""epic_events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from authentication.views import ChangePasswordView
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import routers

from api.views import ClientsViewset, ContractsViewset, EventsViewset


admin.site.site_title = 'CRM Epic Events'
admin.site.site_header = 'CRM Epic Events'
admin.site.index_title = 'Administration'


router = routers.SimpleRouter()
router.register('clients', ClientsViewset, basename='clients')
router.register('contracts', ContractsViewset, basename='Contracts')
router.register('events', EventsViewset, basename='Events')

urlpatterns = [
    path('gestion/', admin.site.urls),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('', RedirectView.as_view(url='login/')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls), name='clients'),
    path('', include(router.urls), name='contracts'),
]
