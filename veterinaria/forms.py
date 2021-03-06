from django import forms
from .models import Usuario, Reserva, Animal

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirma contraseña", widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'rut', 'email', 'password1', 'password2']

class RegistroReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre_animal', 'especie', 'raza', 'servicio', 'telefono', 'fecha_atencion', 'comentario']
        widgets = {
        'fecha_atencion': forms.DateInput(format=('%m/%d/%Y'), attrs={'type':'date'}),
        }

class RegistroAnimalForm(forms.ModelForm):
    opcionesEsterilizado = (
        (True, 'SI'),
        (False, 'NO'),
    )
    esterilizado = forms.ChoiceField(choices = opcionesEsterilizado)
    class Meta:
        model = Animal
        fields = ['nombre', 'especie', 'raza', 'peso', 'sexo', 'color', 'edad', 'esterilizado']