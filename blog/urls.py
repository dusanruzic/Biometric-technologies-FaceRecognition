"""upravnik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from .views import ZgradaListView, ZgradaDetailView, StanarListView, StanarDetailView, ReklamaListView, ReklamaDetailView, OglasivacListView, OglasivacDetailView, RacuniStanariListView, RacuniStanariDetailView, RacuniReklamaiListView, RacunireklamaiDetailView
from blog import views

urlpatterns = [
path('blinkstat', views.blinkstat, name = 'blinkstat'),
path('blink', views.blinkanalysis, name = 'blink'),

path('login', views.loginPage, name = 'login'),
path('logout', views.logoutUser, name = 'logout'),
path('register', views.register, name = 'register'),
path('kreirajracune/<int:pk>/', views.kreirajracune, name='kreirajracune'),    
path('zgrade', ZgradaListView.as_view(), name='zgrada-list'),
path('zgrade/<int:pk>/', ZgradaDetailView.as_view(), name='zgrada-detail'),

path('stanari', StanarListView.as_view(), name='stanar-list'),
path('stanari/<int:pk>/', StanarDetailView.as_view(), name='stanar-detail'),

path('reklame', ReklamaListView.as_view(), name='reklama-list'),
path('reklame/<int:pk>/', ReklamaDetailView.as_view(), name='reklama-detail'),

path('oglasivaci', OglasivacListView.as_view(), name='oglasivac-list'),
path('oglasivac/<int:pk>/', OglasivacDetailView.as_view(), name='oglasivac-detail'),

path('racunistanari', RacuniStanariListView.as_view(), name='racunistanari-list'),
path('racunistanari/<int:pk>/', RacuniStanariDetailView.as_view(), name='racunistanari-detail'),

path('racunireklama', RacuniReklamaiListView.as_view(), name='racunireklama-list'),
path('racunireklama/<int:pk>/', RacunireklamaiDetailView.as_view(), name='racunireklama-detail'),
]