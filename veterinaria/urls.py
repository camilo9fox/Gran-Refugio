from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('inicio', views.Inicio.as_view(), name="inicio"),
    path('conocenos', views.Conocenos.as_view(), name="conocenos"),
    path('urgencias', views.Urgencias.as_view(), name="urgencias"),
    path('consulta', views.Consulta.as_view(), name="consulta"),
    path('registro', views.RegistroUsuario, name="registro"),
    path('reserva', views.Reservar, name="reserva"),
    path('panel', views.Panel, name="panel"),
    path('login', views.Logear, name="login"),
    path('logout', views.Deslogear, name="logout"),
]