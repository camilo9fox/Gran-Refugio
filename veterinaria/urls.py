from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('inicio', views.Inicio.as_view(), name="inicio"),
    path('conocenos', views.Conocenos.as_view(), name="conocenos"),
    path('urgencias', views.Urgencias.as_view(), name="urgencias"),
    path('consulta', views.Consulta.as_view(), name="consulta"),
    path('registro', views.RegistroUsuario, name="registro"),
    path('estadisticas', views.Estadisticas, name="estadisticas"),
    path('crud', views.Crud, name="crud"),
    path('reserva', views.Reservar, name="reserva"),
    path('panel', views.Panel, name="panel"),
    path('login', views.Logear, name="login"),
    path('logout', views.Deslogear, name="logout"),
    path('agregar', views.agregarUsuario, name="agregar"),
    path('buscar', views.buscar_para_modificar, name="buscar"),
    path('mostrar', views.mostrar_para_modificar, name="mostrar"),
    path('modificar', views.modificarUsuario, name="modificar"),
    path('listar', views.listarUsuarios, name="listar"),
    path('eliminar', views.eliminarUsuario, name="eliminar"),
    path('cambiar_contraseña', views.cambiarContraseña, name="cambiar_contraseña"),
    path('registrar_animal', views.RegistroAnimal, name="registrar_animal"),
    path('mis_pacientes', views.mostrarPacientes, name="mis_pacientes"),
    path('citas_pendientes', views.mostrarCitas, name="citas_pendientes"),
    path('vacunas_pendientes', views.mostrarVacunas, name="vacunas_pendientes"),
    path('video_consulta', views.videoConsultas, name="video_consulta"),
]