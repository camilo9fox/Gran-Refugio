from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, CreateView
from .models import Usuario, Reserva
from .forms import UserRegisterForm, RegistroReservaForm
# Create your views here.

class Inicio(TemplateView):
    template_name = 'vet/inicio.html'

class Conocenos(TemplateView):
    template_name = 'vet/conocenos.html'

class Urgencias(TemplateView):
    template_name = 'vet/urgencias.html'

class Consulta(TemplateView):
    template_name = 'vet/consulta.html'

def Reservar(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            myForm = RegistroReservaForm(request.POST)
            if myForm.is_valid():
                reserva = Reserva()
                reserva.cliente = request.user
                reserva.nombre_animal  = myForm.cleaned_data['nombre_animal']
                reserva.especie        = myForm.cleaned_data['especie']
                reserva.raza           = myForm.cleaned_data['raza']
                reserva.servicio       = myForm.cleaned_data['servicio']
                reserva.fecha_atencion = myForm.cleaned_data['fecha_atencion']
                reserva.telefono       = myForm.cleaned_data['telefono']
                reserva.comentario     = myForm.cleaned_data['comentario']
                reserva.save()
                servicio = reserva.servicio
                messages.success(request, f'Tu reserva se ha realizado con exito, te contactaremos el dia antes de la {servicio}')
        else:
            myForm = RegistroReservaForm()
        context = {'form':myForm}
        return render(request, 'vet/reserva.html', context)
    else:
        messages.error(request, 'Debes logearte para poder hacer una reserva')
        return redirect('login')

def RegistroUsuario(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    else:
        if request.method == 'POST':
            myForm = UserRegisterForm(request.POST)
            if myForm.is_valid():
                codigo = request.POST['txtCodigo']
                clave1 = myForm.cleaned_data['password1']
                clave2 = myForm.cleaned_data['password2']
                if clave1 == clave2:
                    if codigo == 'SUPERUSER24':
                        myForm.Meta.model.objects.create_superuser(
                            myForm.cleaned_data['rut'],
                            myForm.cleaned_data['email'],
                            myForm.cleaned_data['nombre'],
                            myForm.cleaned_data['apellido'],
                            myForm.cleaned_data['password1'],
                        )
                    else:
                        myForm.Meta.model.objects.create_user(
                            myForm.cleaned_data['rut'],
                            myForm.cleaned_data['email'],
                            myForm.cleaned_data['nombre'],
                            myForm.cleaned_data['apellido'],
                            myForm.cleaned_data['password1'],
                        )
                    nombre = myForm.cleaned_data['nombre']
                    messages.success(request, f"Usuario {nombre} creado")
                    return redirect('urgencias')
                else:
                    messages.error(request, 'Las contraseñas deben coincidir')
        else:
            myForm = UserRegisterForm()
    context = {'form' : myForm}
    return render(request, 'vet/registro.html', context)

@login_required(login_url = 'login')
def Panel(request):
    reservas = Reserva.objects.all()
    usuario  = request.user
    cantidad_reservas = 0
    proxima_visita = '0/0/0000'
    for reserva in reservas:
        if usuario.rut == reserva.cliente.rut:
            cantidad_reservas+=1
            proxima_visita = reserva.fecha_atencion
    context = {'visita' : proxima_visita, 'usuario' : usuario, 'reservas' : cantidad_reservas}
    return render(request, 'vet/panel.html', context)
    
    
def Logear(request):
    if request.user.is_authenticated:
        return redirect('consulta')
    if request.method == 'POST':
        rut = request.POST['rut']
        contraseña = request.POST['contraseña']

        user = authenticate(request, rut=rut, password=contraseña)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.nombre}')
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrecto')

    context = {}
    return render(request, 'vet/login.html', context)

def Deslogear(request):
    logout(request)
    messages.success(request, 'Sesion terminada')
    return redirect('login')




