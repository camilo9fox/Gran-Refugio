from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, CreateView
from .models import Usuario, Reserva, Animal
from .forms import UserRegisterForm, RegistroReservaForm, RegistroAnimalForm
# Create your views here.

class Inicio(TemplateView):
    template_name = 'vet/inicio.html'

class Conocenos(TemplateView):
    template_name = 'vet/conocenos.html'

class Urgencias(TemplateView):
    template_name = 'vet/urgencias.html'

class Consulta(TemplateView):
    template_name = 'vet/consulta.html'

def RegistroAnimal(request):
    if request.method == 'POST':
        myForm = RegistroAnimalForm(request.POST)
        if myForm.is_valid():
            animal = Animal()
            animal.nombre = myForm.cleaned_data['nombre']
            animal.especie = myForm.cleaned_data['especie']
            animal.raza = myForm.cleaned_data['raza']
            animal.peso = myForm.cleaned_data['peso']
            animal.sexo = myForm.cleaned_data['sexo']
            animal.color = myForm.cleaned_data['color']
            animal.edad = myForm.cleaned_data['edad']
            animal.id_animal_propietario = 1
            animal.id_animal_veterinario = 2
            animal.esterilizado = myForm.cleaned_data['esterilizado']
            animal.foto = request.FILES['foto']
            animal.save()
            messages.success(request, 'Genial registro completado')
        else:
            messages.error(request, 'Error')
    else:
        myForm = RegistroAnimalForm()
    context = {'form' : myForm}
    return render(request, 'vet/registro_animal.html', context)

@login_required(login_url = 'login')
def Estadisticas(request):
    return render(request, 'vet/estadisticas.html', {})

@login_required(login_url = 'login')
def Crud(request):
    return render(request, 'vet/crud/crud.html', {})

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
                            'admin'
                        )
                    elif codigo == 'VETUSER23':
                        myForm.Meta.model.objects.create_user(
                            myForm.cleaned_data['rut'],
                            myForm.cleaned_data['email'],
                            myForm.cleaned_data['nombre'],
                            myForm.cleaned_data['apellido'],
                            myForm.cleaned_data['tipo'],
                            myForm.cleaned_data['password1'],
                            'veterinario'
                        )
                    else:
                        myForm.Meta.model.objects.create_user(
                            myForm.cleaned_data['rut'],
                            myForm.cleaned_data['email'],
                            myForm.cleaned_data['nombre'],
                            myForm.cleaned_data['apellido'],
                            myForm.cleaned_data['tipo'],
                            myForm.cleaned_data['password1'],
                            'cliente'
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

@login_required(login_url = 'login')
def agregarUsuario(request):
    if request.user.is_superuser == False:
        return redirect('panel')
    if request.method == 'POST':
        usuario = Usuario()
        clave1  = request.POST['pass1']
        clave2  = request.POST['pass2']
        tipo    = request.POST['tipo_usuario']
        if clave1 == clave2:
            if tipo == 'cliente' or tipo == 'funcionario':
                usuario.is_superuser = False
                usuario.is_staff     = False
            else:
                usuario.is_superuser = True
                usuario.is_staff     = True
            usuario.tipo      = tipo
            usuario.nombre    = request.POST['nombre']
            usuario.apellido  = request.POST['apellido']
            usuario.rut  = request.POST['rut']
            usuario.email     = request.POST['email']
            usuario.estado    = request.POST['estado']
            usuario.set_password(clave1)
            usuario.save()
            messages.success(request, 'Muy bien usuario agregado')
        else:
            messages.error(request, 'Las contraseñas no coinciden')

    return render(request, 'vet/crud/agregar.html', {})

@login_required(login_url = 'login')
def buscar_para_modificar(request):
    if request.user.is_superuser == False:
        return redirect('panel')
    return render(request, 'vet/crud/buscar.html', {})

@login_required(login_url = 'login')
def mostrar_para_modificar(request):
    if request.user.is_superuser == False:
        return redirect('panel')
    try:
        if request.method == 'POST':
            rut = request.POST['rut']
            usuario  = Usuario.objects.get(rut = rut)
            context = {'usuario' : usuario}
        return render(request, 'vet/crud/modificar.html', context)
    except ObjectDoesNotExist:
        return render(request, 'vet/error/error201.html', {})

@login_required(login_url = 'login')
def modificarUsuario(request):
    if request.user.is_superuser == False:
        return redirect('panel')
    if request.method == 'POST':
        id = request.POST['idUsuario']
        usuario  = Usuario.objects.get(id = id)
        clave1   = request.POST['pass1']
        clave2   = request.POST['pass2']
        tipo     = request.POST['tipo_usuario']
        if clave1 == clave2:
            if tipo == 'cliente' or tipo == 'funcionario':
                usuario.is_superuser = False
                usuario.is_staff     = False
            else:
                usuario.is_superuser = True
                usuario.is_staff     = True
            usuario.tipo      = tipo
            usuario.rut  = request.POST['rut']
            usuario.nombre    = request.POST['nombre']
            usuario.apellido  = request.POST['apellido']
            usuario.username  = request.POST['username']
            usuario.email     = request.POST['email']
            usuario.estado    = request.POST['estado']
            usuario.set_password(clave1)
            usuario.save()
            messages.success(request, 'Muy bien usuario modificado')
        else:
            messages.error(request, 'Las contraseñas no coinciden')

    return render(request, 'vet/crud/modificar.html', {})

@login_required(login_url = 'login')
def listarUsuarios(request):
    usuarios = Usuario.objects.all()
    context  = {'usuarios' : usuarios}
    return render(request, 'vet/crud/listar.html', context)

@login_required(login_url = 'login')
def eliminarUsuario(request):
    if request.user.is_superuser == False:
        return redirect('panel')
    try:
        if request.method == 'POST':
            rut = request.POST['rut']
            usuario  = Usuario.objects.get(rut = rut)
            usuario.delete()
            messages.success(request, 'Usuario eliminado')
        return render(request, 'vet/crud/eliminar.html', {})
    except ObjectDoesNotExist:
        return render(request, 'vet/error/error201.html', {})

def cambiarContraseña(request):
    if request.method == 'POST':
        ex_pass1 = request.POST['exPass1']
        ex_pass2 = request.POST['exPass2']
        if ex_pass1 == ex_pass2:
            usuario = request.user
            if usuario.check_password(ex_pass1):
                new_pass1 = request.POST['newPass1']
                new_pass2 = request.POST['newPass2']
                if new_pass1 == ex_pass1:
                    messages.error(request, 'La contraseña nueva no debe ser la misma que la actual, prueba con otra')
                else:
                    if new_pass1 == new_pass2:
                        usuario.set_password(new_pass1)
                        usuario.save()
                        messages.success(request, 'Muy bien tu contraseña se modifico con exito.')  
                    else:
                        messages.error(request, 'Las contraseñas deben coincidir')
            else:
                messages.error(request, 'La contraseña ingresada no coincide con tu contraseña actual')
        else:
            messages.error(request, 'Las contraseñas deben coincidir')    
    return render(request, 'vet/cambiar_contraseña.html', {})   


def mostrarPacientes(request):
    if request.user.tipo == 'funcionario':
        usuario = request.user
        animales  = Animal.objects.all()
        for animal in animales:
            if animal.id_animal_veterinario == usuario.id:
                context = {'animal' : animal}
            else:
                context = {'animal' : 'No tienes ningun paciente'}
        return render(request, 'vet/mis_pacientes.html', context)
    else:
        return redirect('inicio')

def mostrarCitas(request):
    return render(request, 'vet/citas_pendientes.html', {})

def mostrarVacunas(request):
    return render(request, 'vet/vacunas_pendientes.html', {})

def videoConsultas(request):
    return render(request, 'vet/video_consultas.html', {})




