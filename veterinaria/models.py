from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UsuarioManager(BaseUserManager):
    def _create_user(self, rut, email, nombre, apellido, password, tipo, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener correo electronico")
        usuario = self.model(
            rut = rut,
            email = self.normalize_email(email),
            nombre = nombre,
            apellido = apellido,
            tipo = tipo,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        usuario.set_password(password)
        usuario.save(using=self.db)
        return usuario
    
    def create_user(self, rut, email, nombre, apellido, password, tipo, **extra_fields):
        usuario = self._create_user(
            rut,
            email,
            nombre,
            apellido,
            password,
            tipo,
            False,
            False,
            **extra_fields
        )

    def create_superuser(self, rut, email, nombre, apellido, password, tipo, **extra_fields):
        usuario = self._create_user(
            rut,
            email,
            nombre,
            apellido,
            password,
            tipo,
            True,
            True,
            **extra_fields
        )


class Usuario(AbstractBaseUser, PermissionsMixin):
    rut              =  models.CharField('Rut', unique = True, max_length = 100)
    email            =  models.EmailField('Correo electronico', unique = True, max_length = 250)
    nombre           =  models.CharField('Nombre completo', max_length = 200)
    apellido         =  models.CharField('Apellidos', max_length = 200)
    fecha_nacimiento =  models.DateField('Fecha de nacimiento', blank = True, null = True)
    estado           =  models.CharField('Estado', max_length = 50, default = 'DISPONIBLE')
    tipo             =  models.CharField('Tipo de usuario', max_length = 50, default = 'cliente')
    is_active        =  models.BooleanField(default = True)
    is_staff         =  models.BooleanField(default = False)
    objects          =  UsuarioManager()

    USERNAME_FIELD  = 'rut'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido']

    def __str__(self):
        return "rut: " + self.rut + ", " + "Nombre: " + self.nombre + ", " + "Estado: " + self.estado


class Reserva(models.Model):
    SERVICIOS = (
        ('Por defecto', 'Elige una opcion'),
        ('Consulta', 'Consulta, vacunas, desparasitación o chip'),
        ('Examen', 'Exámenes de laboratorio'),
        ('Imagenología', 'Imagenología (Ecografía, Radiografía, otros)'),
        ('Peluqueria', 'Peluqueria, baño, corte de uñas'),
        ('Esterilización', 'Esterilización'),
        ('Otro', 'Otro (Puedes añadir informacion extra)'),
    )
    id_reserva       =  models.AutoField(primary_key = True)
    cliente          =  models.ForeignKey(Usuario, on_delete = models.CASCADE)
    nombre_animal    =  models.CharField('Nombre animal', max_length = 50)
    especie          =  models.CharField('Especie', max_length = 50)
    raza             =  models.CharField('Raza', max_length = 50)
    telefono         =  models.CharField('Numero de telefono', max_length = 9)
    servicio         =  models.CharField('Servicio', max_length = 150, choices = SERVICIOS, default = SERVICIOS[0][0])
    fecha_atencion   =  models.DateField('Fecha de atencion')
    comentario       =  models.CharField('Informacion extra', max_length = 250)

    def __str__(self):
        return "Rut cliente: " + self.cliente.rut + ", " + "Nombre animal: " + self.nombre_animal + ", " + "Telefono: " + self.telefono + ", " + "Servicio: " + self.servicio


class Animal(models.Model):
    SEXOS = (
        ('Por defecto', 'Elige una opcion'),
        ('Hembra', 'H'),
        ('Macho', 'M'),
    )
    id_animal                =  models.AutoField(primary_key = True)
    id_animal_propietario    =  models.IntegerField('Id propietario')
    id_animal_veterinario    =  models.IntegerField('Id veterinario')
    foto                     =  models.ImageField('Foto', upload_to = "fotos_pacientes", null = True, blank = True)
    nombre                   =  models.CharField('Nombre animal', max_length = 50)
    especie                  =  models.CharField('Especie', max_length = 50)
    raza                     =  models.CharField('Raza', max_length = 50)
    peso                     =  models.FloatField('Peso')
    sexo                     =  models.CharField('Sexo', max_length = 20, choices = SEXOS, default = SEXOS[0][0])
    color                    =  models.CharField('Color', max_length = 50)
    edad                     =  models.IntegerField('Edad')
    esterilizado             =  models.BooleanField('Esterilizado', default = False)